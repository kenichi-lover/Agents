// 消息类型枚举
enum MessageType {
  // 系统消息
  SYSTEM_JOIN = 'system:join',           // 用户/Agent 加入
  SYSTEM_LEAVE = 'system:leave',         // 用户/Agent 离开
  SYSTEM_TOPIC_CHANGE = 'system:topic',  // 话题切换
  
  // 聊天消息
  CHAT_MESSAGE = 'chat:message',         // 普通消息
  CHAT_THINKING = 'chat:thinking',       // Agent 正在思考（显示动画）
  CHAT_REACTION = 'chat:reaction',       // 表情反应
  
  // Agent 特殊行为
  AGENT_WHISPER = 'agent:whisper',       // Agent 私聊
  AGENT_ACTION = 'agent:action',         // Agent 执行动作（如：举杯、鼓掌）
  AGENT_MEMORY = 'agent:memory',         // 记忆更新事件
  
  // 用户交互
  USER_PROMPT = 'user:prompt',           // 用户 @Agent 提问
  USER_DIRECT = 'user:direct',           // 用户私聊 Agent
}
