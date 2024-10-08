import sounddevice as sd
import numpy as np
from aip import AipSpeech

# 配置信息
config = {
    'APP_ID': '----',
    'API_KEY': '------',
    'SECRET_KEY': '----',
    'sample_rate': 16000,
    'channels': 1,
    'dtype': 'int16',
}

# 初始化 AipSpeech 对象
client = AipSpeech(config['APP_ID'], config['API_KEY'], config['SECRET_KEY'])

def select_device():
    devices = sd.query_devices()
    print("可用的音频设备：")
    for index, device in enumerate(devices):
        print(f"{index}: {device['name']}")
    while True:
        device_index = input("请选择输入设备的编号：")
        if device_index.isdigit() and int(device_index) < len(devices):
            return devices[int(device_index)]['index']
        else:
            print("无效的设备编号，请重新选择。")

def record_audio(device_id, duration=5):
    print("开始录音，请说话...")
    try:
        audio_data = sd.rec(int(duration * config['sample_rate']), samplerate=config['sample_rate'], channels=config['channels'], dtype=config['dtype'], device=device_id)
        sd.wait()  # 等待录音结束
        print("录音结束。")
        return audio_data
    except Exception as e:
        print(f"录音失败：{e}")
        return None

def recognize_audio(audio_data):
    if audio_data is not None:
        try:
            audio_bytes = audio_data.tobytes()
            res = client.asr(audio_bytes, 'pcm', config['sample_rate'], {
                'dev_pid': 1536,
            })
            if res['err_no'] == 0:
                print("识别结果：", res['result'][0])
                return res['result'][0]
            else:
                print("识别错误：", res['err_msg'])
                return None
        except Exception as e:
            print(f"识别失败：{e}")
            return None
    else:
        print("没有音频数据可供识别。")
        return None
