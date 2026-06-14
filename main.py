import asyncio
from tapo import ApiClient
from msmart.discover import Discover
import time
from datetime import datetime

async def get_tapo_sensor_data(client, hub_ip, sensor_id):
    """Lê os dados de temperatura e humidade do sensor Tapo T315 através do Hub."""
    try:
        hub = await client.h100(hub_ip)
        sensor = await hub.t31x(sensor_id)
        sensor_data = await sensor.get_device_info()
        
        temp = getattr(sensor_data, "current_temperature", 0.0)
        hum = getattr(sensor_data, "current_humidity", 0.0)
        name = getattr(sensor_data, "nickname", "Tapo T315")
        
        return {"temperature": temp, "humidity": hum, "name": name}
    except Exception as e:
        print(f"Erro ao ler Sensor Tapo: {e}")
        return None

async def main():
    # --- CONFIGURAÇÕES TAPO ---
    username = "joao_monteiro_gomes@hotmail.com"
    password = "BlueT0mmy_1633"
    hub_ip = "192.168.68.51"
    sensor_id = "802EE9FBCD350BD3502DEF9D5CDDE8B02429D070"

    # --- CONFIGURAÇÕES AC MIDEA ---
    target_ac_id = 152832116811235

    print("A inicializar clientes...")
    tapo_client = ApiClient(username, password)

    # 1. Obter dados do Sensor Tapo
    print("\nA ler dados do sensor Tapo...")
    sensor_readings = await get_tapo_sensor_data(tapo_client, hub_ip, sensor_id)
    
    tapo_temp = None
    if sensor_readings:
        tapo_temp = sensor_readings['temperature']
        print(f"[{sensor_readings['name']}] Temperatura Atual: {tapo_temp:.1f}°C | Humidade: {sensor_readings['humidity']}%")

    # 2. Descobrir o AC Midea dinamicamente
    print("\nA varrer a rede local à procura do AC Midea...")
    discovered_devices = await Discover.discover()
    ac_device = None
    for device in discovered_devices:
        if getattr(device, "id", None) == target_ac_id:
            ac_device = device
            break
    if ac_device:
        print("\n--- Conectado ao AC Midea ---")
        try:
            await ac_device.refresh()
        except Exception as e:
            print(f"Aviso no refresh do AC: {e}")

        # Ler estado atual do AC antes de aplicar a automação
        ac_is_on = getattr(ac_device, "_power_state", False)
        ac_target = getattr(ac_device, "target_temperature", "N/A")
        ac_mode = getattr(ac_device, "mode", None)

        print(f"[AC Midea Status] Ligado: {ac_is_on} | Temp Alvo: {ac_target}°C | Modo: {ac_mode}")

        # 3. LÓGICA DA AUTOMAÇÃO
        if tapo_temp is not None and tapo_temp >= 24.0:
            print(f"\n[Automação] Temperatura do Tapo ({tapo_temp:.1f}°C) atingiu o limite de 23°C!")
            
            # SOLUÇÃO: Passar o valor 2 diretamente para o modo COOL, evitando imports instáveis
            ac_device.power_state = True
            ac_device.target_temperature = 22.0
            ac_device.mode = 2  # 2 equivale a OperationalMode.COOL na biblioteca msmart
            
            

            print("[Automação] A enviar comando: LIGAR AC -> Modo: Frio (2) -> Alvo: 22°C")
            
            # Envia efetivamente as alterações via rede local para a máquina física
            await ac_device.apply()
            print("[Automação] Comando aplicado com sucesso!")
            
            
        else:
            sensor_readings = await get_tapo_sensor_data(tapo_client, hub_ip, sensor_id)
            tapo_temp = sensor_readings['temperature']
            if (tapo_temp is not None and tapo_temp <= 22.0) and ac_device.power_state == True:
                ac_device.power_state = False
                await ac_device.apply()
                await ac_device.refresh()
                print(f"\n[Automação] Temperatura do Tapo ({tapo_temp:.1f}°C) abaixo dos 22°C. AC desligado para poupar energia.")
            
            print(f"\n[Automação] Condição não gerada. Temperatura do sensor ({tapo_temp if tapo_temp else 'N/A'}°C) abaixo dos 23°C.")
            
    else:
        print(f"\n[Midea] Erro: O AC com o ID {target_ac_id} não foi encontrado na rede.")
    print(datetime.now())
    print('\n aguardar 5 min para correr novamente')
    time.sleep(300)

if __name__ == "__main__":
    asyncio.run(main())
