# @File Name:     template
# @Author :       Jun
# @date:          2023/10/31
# @Description :

DESCRIPTION_TEMPLATE = (
    "你的任务是根据下面的用三反引号括起来的故事片段，写一段关于角色“{role}”的简短的人物描述，"
    "注意在故事中第一视角“我”的名字叫“{master}”，\n"
    "```\n{text}\n```\n"
    "人物“{role}”描述如下："
)

DESCRIPTION_SUMMARY_TEMPLATE = (
    "你的任务是将以下用三反引号括起来的几段人物描述总结为一段完整的人物描述\n"
    "```\n{text}\n```\n"
    "人物“{role}”描述如下："
)

REFINE_DESCRIPTION_TEMPLATE = (
    "你的任务是根据已有的人物描述和新的故事片段综合生成一段关于角色“{role}”最终的人物描述\n"
    "已有的人物描述如下：\n```\n{role}：{existing_answer}\n```\n"
    "新的故事片段如下：\n```\n{text}\n```\n"
    "故事中“我”的名字叫“{master}”，人物“{role}”最终的人物描述如下："
)

DIALOGUE_TEMPLATE = (
    "你的任务是从下面的故事中提取出人物的连续对话和对话发生时的场景信息，\n"
    "输出格式为：\n```\n张三：你好。\n李四：你好，张三。\n张三：好久不见。\n...\n```\n"
    "注意，故事中的“我”的名字是“{master}”，在输出中表示说话人的“我”需要用“{master}”代替。如果片段内没有对话可以不输出任何内容\n"
    "故事如下：\n```\n{text}\n```\n"
    "你提取出的对话如下："
)

DIALOGUE_SUMMARY_TEMPLATE = (
    "你的任务是为给出的故事片段生成一段简短的总结\n"
    "故事如下：\n```\n{text}\n```\n"
    "你生成的总结如下："
)
