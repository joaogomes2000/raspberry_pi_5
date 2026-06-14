import asyncio
from tapo import ApiClient
from msmart.device import AirConditioner  # Importa diretamente a classe do AC

async def get_tapo_sensor_data(client, hub_ip, sensor_id):
    """Lê os dados de temperatura e humidade do sensor Tapo T315."""
    try:
        hub = await client.h100(hub_ip)
        sensor = await hub.t31x(sensor_id)
        sensor_data = await sensor.get_device_info()
        
        temp = getattr(sensor_data, "current_temperature", None)
        hum = getattr(sensor_data, "current_humidity", None)
        name = getattr(sensor_data, "nickname", "Tapo T315")
        
        return {"temperature": temp, "humidity": hum, "name": name}
    except Exception as e:
        print(f"Erro ao ler Sensor Tapo: {e}")
        return None

async def main():
    # --- CONFIGURAÇÕES ---
    username = "joao_monteiro_gomes@hotmail.com"
    password = "BlueT0mmy_1633"
    hub_ip = "192.168.68.51"
    sensor_id = "802EE9FBCD350BD3502DEF9D5CDDE8B02429D070"
    
    # Configurações estáticas do AC Midea (evita problemas de rede do Docker no Mac)
    target_ac_id = 152832116811235
    target_ac_ip = "192.168.68.56"

    print("A inicializar clientes...")
    tapo_client = ApiClient(username, password)

    # LOOP INFINITO PARA O DOCKER
    while True:
        try:
            print("\n--- A iniciar verificação da rotina ---")
            
            # 1. Ler Sensor Tapo
            sensor_readings = await get_tapo_sensor_data(tapo_client, hub_ip, sensor_id)
            tapo_temp = None
            if sensor_readings and sensor_readings['temperature'] is not None:
                tapo_temp = sensor_readings['temperature']
                print(f"[{sensor_readings['name']}] Temperatura Atual: {tapo_temp:.1f}°C")
            else:
                print("Não foi possível obter uma leitura válida do Tapo. A saltar esta passagem.")
                await asyncio.sleep(300)
                continue

            # 2. Ligação DIRETA ao AC por IP (Bypassa as limitações de rede do Docker Mac)
            print(f"A conectar diretamente ao AC Midea no IP {target_ac_ip}...")
            ac_device = AirConditioner(device_id=target_ac_id, ip=target_ac_ip, port=6444)
            
            # Força o handshake/autenticação com o IP fornecido
            await ac_device.refresh()
            
            ac_is_on = getattr(ac_device, "power", False)
            ac_target = getattr(ac_device, "target_temperature", "N/A")
            ac_mode = getattr(ac_device, "mode", "N/A")
            print(f"[AC Status] Ligado: {ac_is_on} | Temp Alvo: {ac_target}°C | Modo: {ac_mode}")

            # 3. LÓGICA DA AUTOMAÇÃO
            if tapo_temp >= 24.0:
                print(f"[Automação] Temperatura alta ({tapo_temp:.1f}°C >= 24°C)! A ligar AC no frio...")
                ac_device.power = True
                ac_device.target_temperature = 22.0
                ac_device.mode = 2  # Modo COOL
                await ac_device.apply()
                print("[Automação] Comando aplicado com sucesso!")
                
            elif tapo_temp <= 22.0:
                if ac_is_on:
                    print(f"[Automação] Temperatura baixa ({tapo_temp:.1f}°C <= 22°C). A desligar AC...")
                    ac_device.power = False
                    await ac_device.apply()
                    print("[Automação] AC desligado com sucesso.")
                else:
                    print(f"[Automação] Temperatura a {tapo_temp:.1f}°C. AC já se encontra desligado.")
            else:
                print(f"[Automação] Temperatura confortável ({tapo_temp:.1f}°C). Nada a fazer.")
                
        except Exception as e:
            print(f"Erro no ciclo de automação: {e}")
            
        print("\nA aguardar 5 minutos para a próxima verificação...")
        await asyncio.sleep(300)

if __name__ == "__main__":
    asyncio.run(main())