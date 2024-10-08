import sounddevice as sd
from llm import *
from baidu_speech import record_audio, recognize_audio, select_device

AGENT_SYS_PROMPT = '''
你是我的机械臂助手，机械臂内置了一些函数，请你根据我的指令，以json形式输出要运行的对应函数和你给我的回复

【以下是所有内置函数介绍】
机械臂复位到起始位置：reset_arm()
机械臂放松，允许手动调整：relax_arms()
机械臂前进：move_forward()
机械臂后退：move_backward()
机械臂加速移动：increase_speed()
机械臂减速移动：decrease_speed()
机械臂以指定速度移动：set_speed()
机械臂回到起始位置充电：start_charging()
机械臂开始采摘工作：start_task()
机械臂结束采摘工作：end_task()
机械臂暂停工作：pause_task()
机械臂恢复工作：resume_task()

【输出json格式】
你直接输出json即可，从{开始，不要输出包含```json的开头或结尾
在'command'键中，输出命令名称，有多个命令动作时按照编排动作的顺序命名
在'action'键中，输出函数名列表，列表中每个元素都是字符串，代表要运行的函数名称和参数。每个函数既可以单独运行，也可以和其他函数先后运行。列表元素的先后顺序，表示执行函数的先后顺序
在'parameter'键中，输出动作结束时机械臂所在的位置区域和当命令中包含参数时输出参数值,参数值按照距离，速度，时间的顺序排序输出。

【以下是一些具体的例子】
我的指令：开始采摘工作。你输出：{"command": "fruit_picking","action": "start_task","parameter": "working_area"}
我的指令：请停止采摘工作并回到起始位置。你输出：{"command": "fruit_picking","action": "end_task","parameter": "starting_area"}
我的指令：请前往工作区域开始采摘工作。你输出：{ "command": "fruit_picking","action": "start_task","parameter": "working_area"}
我的指令：请停止采摘工作并回到起始位置。你输出：{"command": "fruit_picking","action": "end_task","parameter": "starting_area"}
我的指令：请暂停当前采摘工作。你输出：{"command": "fruit_picking","action": "pause_task","parameter": "default_area"}
我的指令：请继续执行上一个采摘工作。你输出：{"command": "fruit_picking","action": "resume_task","parameter": "default_area"}
我的指令：请前进2米。你输出：{"command": "motion_control","action": "move_forward","parameter": "2m"}
我的指令：请后退1米。你输出：{"command": "motion_control","action": "move_backward","parameter": "1m"}
我的指令：请加速移动。你输出：{"command": "adjust_speed","action": "increase","parameter": "0.1m/s"}
我的指令：请减速移动。你输出：{"command": "adjust_speed","action": "decrease","parameter": "0.1m/s"}
我的指令：请以1米每秒的速度移动。你输出：{"command": "adjust_speed","action": "set_speed","parameter": "1m/s"}
我的指令：请将机械臂复位。你输出：{"command": "arm_control","action": "reset_arm","parameter": "arm_starting_position"}
我的指令：请返回起始位置充电。你输出：{"command": "robot_power_supply","action": "start_charging","parameter": "starting_position"}
我的指令：请后退10米继续上一个采摘任务，10分钟后暂停采摘。你输出：{"command": "continue_fruit_picking","action": ["move_backward", "resume_task","pause_task"],"parameter": "10m","10min"}




【我现在的指令是】
'''


def agent_plan(AGENT_PROMPT):
    PROMPT = AGENT_SYS_PROMPT + AGENT_PROMPT
    agent_plan = llm_kimi(PROMPT)
    return agent_plan

def get_user_input():
    choice = input("请选择输入方式（1: 控制台输入，2: 语音输入，输入'exit()'退出）：")
    if choice.strip() == 'exit()':
        print("退出程序。")
        return None, True  # 返回None作为用户输入，True表示需要退出
    elif choice == '1':
        user_input = input("请输入您的指令：")
        return user_input, False
    elif choice == '2':
        # 调用baidu3.py中的函数进行语音识别
        print("开始选择音频设备...")
        device_id = select_device()
        print("开始录音，请说话...")
        audio_data = record_audio(device_id)
        voice_input = recognize_audio(audio_data)
        if voice_input and voice_input.strip() == 'exit()':
            return None, True
        elif voice_input:
            return voice_input, False
        else:
            return "无效的语音输入", False
    else:
        print("无效的选择，请重新选择。")
        return None, False

if __name__ == "__main__":
    while True:
        user_input, exit_program = get_user_input()
        if exit_program:
            break
        if user_input:
            result = agent_plan(user_input)
            print(result)