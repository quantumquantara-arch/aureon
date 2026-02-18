#!/usr/bin/env python3
"""
AUREON WEB CHAT INTERFACE BUILDER
==================================
Automatically generates a beautiful web chat interface on startup.
"""

from pathlib import Path


def build_chat_interface(output_dir: str = r"C:\AUREON_AUTONOMOUS\WEB_INTERFACE") -> Path:
    """
    Build a complete web chat interface for AUREON.
    Returns path to the HTML file.
    """
    web_dir = Path(output_dir)
    web_dir.mkdir(exist_ok=True)
    
    html_path = web_dir / "aureon_chat.html"
    
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AUREON • Autonomous Intelligence Interface</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        :root {
            --bg-dark: #0a0a14;
            --bg-medium: #12121e;
            --bg-elevated: #1a1a28;
            --accent-cyan: #00d9ff;
            --accent-purple: #9d4edd;
            --text-primary: #e8e8f0;
            --text-secondary: #a0a0b8;
            --success: #00ff88;
            --warning: #ffaa00;
            --error: #ff4444;
        }
        
        body {
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            background: linear-gradient(135deg, var(--bg-dark) 0%, #0f0f1a 100%);
            color: var(--text-primary);
            min-height: 100vh;
            overflow: hidden;
        }
        
        /* Animated background grid */
        .bg-grid {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: 
                linear-gradient(var(--accent-cyan)22 1px, transparent 1px),
                linear-gradient(90deg, var(--accent-cyan)22 1px, transparent 1px);
            background-size: 50px 50px;
            opacity: 0.03;
            pointer-events: none;
            animation: gridPulse 20s ease-in-out infinite;
        }
        
        @keyframes gridPulse {
            0%, 100% { opacity: 0.03; }
            50% { opacity: 0.06; }
        }
        
        .container {
            position: relative;
            max-width: 1400px;
            margin: 0 auto;
            height: 100vh;
            display: flex;
            flex-direction: column;
            padding: 20px;
        }
        
        /* Header */
        .header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 20px 30px;
            background: var(--bg-elevated);
            border-radius: 16px;
            margin-bottom: 20px;
            border: 1px solid rgba(0, 217, 255, 0.1);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }
        
        .logo {
            display: flex;
            align-items: center;
            gap: 15px;
        }
        
        .logo-icon {
            width: 50px;
            height: 50px;
            background: linear-gradient(135deg, var(--accent-cyan), var(--accent-purple));
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            font-weight: bold;
            animation: logoGlow 3s ease-in-out infinite;
        }
        
        @keyframes logoGlow {
            0%, 100% { box-shadow: 0 0 20px rgba(0, 217, 255, 0.3); }
            50% { box-shadow: 0 0 40px rgba(0, 217, 255, 0.6); }
        }
        
        .logo-text h1 {
            font-size: 28px;
            background: linear-gradient(90deg, var(--accent-cyan), var(--accent-purple));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .logo-text p {
            font-size: 12px;
            color: var(--text-secondary);
            margin-top: 4px;
        }
        
        .status-indicators {
            display: flex;
            gap: 15px;
        }
        
        .status-badge {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 8px 16px;
            background: var(--bg-medium);
            border-radius: 8px;
            font-size: 14px;
        }
        
        .status-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            animation: pulse 2s ease-in-out infinite;
        }
        
        .status-dot.online { background: var(--success); }
        .status-dot.active { background: var(--accent-cyan); }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        /* Chat Container */
        .chat-container {
            flex: 1;
            display: flex;
            flex-direction: column;
            background: var(--bg-elevated);
            border-radius: 16px;
            overflow: hidden;
            border: 1px solid rgba(0, 217, 255, 0.1);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }
        
        .messages {
            flex: 1;
            overflow-y: auto;
            padding: 30px;
            display: flex;
            flex-direction: column;
            gap: 20px;
        }
        
        .message {
            display: flex;
            gap: 15px;
            animation: messageSlideIn 0.3s ease-out;
        }
        
        @keyframes messageSlideIn {
            from {
                opacity: 0;
                transform: translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .message.user {
            flex-direction: row-reverse;
        }
        
        .message-avatar {
            width: 40px;
            height: 40px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            flex-shrink: 0;
        }
        
        .message.user .message-avatar {
            background: linear-gradient(135deg, #667eea, #764ba2);
        }
        
        .message.aureon .message-avatar {
            background: linear-gradient(135deg, var(--accent-cyan), var(--accent-purple));
        }
        
        .message-content {
            max-width: 70%;
            padding: 16px 20px;
            border-radius: 12px;
            line-height: 1.6;
        }
        
        .message.user .message-content {
            background: var(--bg-medium);
            border: 1px solid rgba(102, 126, 234, 0.3);
        }
        
        .message.aureon .message-content {
            background: var(--bg-dark);
            border: 1px solid rgba(0, 217, 255, 0.2);
        }
        
        .message-time {
            font-size: 11px;
            color: var(--text-secondary);
            margin-top: 8px;
        }
        
        .typing-indicator {
            display: none;
            align-items: center;
            gap: 15px;
            padding: 20px 30px;
        }
        
        .typing-indicator.active {
            display: flex;
        }
        
        .typing-dots {
            display: flex;
            gap: 6px;
        }
        
        .typing-dots span {
            width: 8px;
            height: 8px;
            background: var(--accent-cyan);
            border-radius: 50%;
            animation: typingBounce 1.4s infinite;
        }
        
        .typing-dots span:nth-child(2) { animation-delay: 0.2s; }
        .typing-dots span:nth-child(3) { animation-delay: 0.4s; }
        
        @keyframes typingBounce {
            0%, 60%, 100% { transform: translateY(0); }
            30% { transform: translateY(-10px); }
        }
        
        /* Input Area */
        .input-area {
            padding: 25px 30px;
            background: var(--bg-dark);
            border-top: 1px solid rgba(0, 217, 255, 0.1);
        }
        
        .input-container {
            display: flex;
            gap: 15px;
            align-items: flex-end;
        }
        
        .input-wrapper {
            flex: 1;
            position: relative;
        }
        
        #messageInput {
            width: 100%;
            padding: 16px 20px;
            background: var(--bg-medium);
            border: 2px solid rgba(0, 217, 255, 0.2);
            border-radius: 12px;
            color: var(--text-primary);
            font-size: 15px;
            font-family: inherit;
            resize: none;
            max-height: 150px;
            transition: all 0.3s ease;
        }
        
        #messageInput:focus {
            outline: none;
            border-color: var(--accent-cyan);
            box-shadow: 0 0 0 3px rgba(0, 217, 255, 0.1);
        }
        
        #messageInput::placeholder {
            color: var(--text-secondary);
        }
        
        #sendButton {
            padding: 16px 32px;
            background: linear-gradient(135deg, var(--accent-cyan), var(--accent-purple));
            border: none;
            border-radius: 12px;
            color: white;
            font-weight: 600;
            font-size: 15px;
            cursor: pointer;
            transition: all 0.3s ease;
            white-space: nowrap;
        }
        
        #sendButton:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(0, 217, 255, 0.4);
        }
        
        #sendButton:active {
            transform: translateY(0);
        }
        
        #sendButton:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            transform: none;
        }
        
        /* Scrollbar */
        .messages::-webkit-scrollbar {
            width: 8px;
        }
        
        .messages::-webkit-scrollbar-track {
            background: var(--bg-dark);
            border-radius: 4px;
        }
        
        .messages::-webkit-scrollbar-thumb {
            background: var(--accent-cyan);
            border-radius: 4px;
        }
        
        .messages::-webkit-scrollbar-thumb:hover {
            background: var(--accent-purple);
        }
        
        /* Welcome Message */
        .welcome-message {
            text-align: center;
            padding: 60px 30px;
            color: var(--text-secondary);
        }
        
        .welcome-message h2 {
            font-size: 32px;
            color: var(--text-primary);
            margin-bottom: 15px;
            background: linear-gradient(90deg, var(--accent-cyan), var(--accent-purple));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .welcome-message p {
            font-size: 16px;
            margin-bottom: 30px;
        }
        
        .capabilities {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 30px;
            max-width: 800px;
            margin-left: auto;
            margin-right: auto;
        }
        
        .capability {
            padding: 20px;
            background: var(--bg-dark);
            border-radius: 10px;
            border: 1px solid rgba(0, 217, 255, 0.1);
        }
        
        .capability-icon {
            font-size: 24px;
            margin-bottom: 10px;
        }
        
        .capability h3 {
            font-size: 14px;
            color: var(--accent-cyan);
            margin-bottom: 5px;
        }
        
        .capability p {
            font-size: 12px;
            color: var(--text-secondary);
        }
    </style>
</head>
<body>
    <div class="bg-grid"></div>
    
    <div class="container">
        <!-- Header -->
        <div class="header">
            <div class="logo">
                <div class="logo-icon">A</div>
                <div class="logo-text">
                    <h1>AUREON</h1>
                    <p>Autonomous Intelligence System</p>
                </div>
            </div>
            <div class="status-indicators">
                <div class="status-badge">
                    <span class="status-dot online"></span>
                    <span id="brainStatus">Brain: Online</span>
                </div>
                <div class="status-badge">
                    <span class="status-dot active"></span>
                    <span id="capabilityStatus">Fully Active</span>
                </div>
            </div>
        </div>
        
        <!-- Chat Container -->
        <div class="chat-container">
            <div class="messages" id="messages">
                <div class="welcome-message">
                    <h2>Welcome to AUREON</h2>
                    <p>Your autonomous intelligence partner. I can see your screen, control your computer, read files, and browse the web.</p>
                    
                    <div class="capabilities">
                        <div class="capability">
                            <div class="capability-icon">[BRAIN]</div>
                            <h3>Dual AI Brain</h3>
                            <p>OpenAI + DeepSeek working together</p>
                        </div>
                        <div class="capability">
                            <div class="capability-icon">?</div>
                            <h3>Active Hands</h3>
                            <p>Keyboard & mouse control</p>
                        </div>
                        <div class="capability">
                            <div class="capability-icon">[EYE]?</div>
                            <h3>Active Eyes</h3>
                            <p>Screen reading & vision</p>
                        </div>
                        <div class="capability">
                            <div class="capability-icon">?</div>
                            <h3>Deep Knowledge</h3>
                            <p id="fileCount">6,869 files integrated</p>
                        </div>
                        <div class="capability">
                            <div class="capability-icon">[GLOBE]</div>
                            <h3>Web Access</h3>
                            <p>Browse & interact with any site</p>
                        </div>
                        <div class="capability">
                            <div class="capability-icon">?</div>
                            <h3>Vector Memory</h3>
                            <p>Remember everything we discuss</p>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="typing-indicator" id="typingIndicator">
                <div class="message-avatar" style="background: linear-gradient(135deg, var(--accent-cyan), var(--accent-purple));">A</div>
                <div class="typing-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
                <span style="color: var(--text-secondary); font-size: 14px;">AUREON is thinking...</span>
            </div>
            
            <div class="input-area">
                <div class="input-container">
                    <div class="input-wrapper">
                        <textarea 
                            id="messageInput" 
                            placeholder="Message AUREON... (Try: 'take a screenshot', 'open google.com', 'what files do you have?')"
                            rows="1"
                        ></textarea>
                    </div>
                    <button id="sendButton">Send</button>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        const API_URL = 'http://127.0.0.1:8000';
        const messagesDiv = document.getElementById('messages');
        const messageInput = document.getElementById('messageInput');
        const sendButton = document.getElementById('sendButton');
        const typingIndicator = document.getElementById('typingIndicator');
        
        // Auto-resize textarea
        messageInput.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = Math.min(this.scrollHeight, 150) + 'px';
        });
        
        // Send on Enter (Shift+Enter for new line)
        messageInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });
        
        sendButton.addEventListener('click', sendMessage);
        
        function addMessage(text, isUser) {
            // Remove welcome message if present
            const welcome = messagesDiv.querySelector('.welcome-message');
            if (welcome) welcome.remove();
            
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${isUser ? 'user' : 'aureon'}`;
            
            const avatar = document.createElement('div');
            avatar.className = 'message-avatar';
            avatar.textContent = isUser ? 'Y' : 'A';
            
            const content = document.createElement('div');
            content.className = 'message-content';
            content.innerHTML = formatMessage(text);
            
            const time = document.createElement('div');
            time.className = 'message-time';
            time.textContent = new Date().toLocaleTimeString();
            content.appendChild(time);
            
            messageDiv.appendChild(avatar);
            messageDiv.appendChild(content);
            messagesDiv.appendChild(messageDiv);
            
            // Scroll to bottom
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }
        
        function formatMessage(text) {
            // Basic markdown-like formatting
            text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
            text = text.replace(/\*(.*?)\*/g, '<em>$1</em>');
            text = text.replace(/`(.*?)`/g, '<code style="background: var(--bg-medium); padding: 2px 6px; border-radius: 4px;">$1</code>');
            text = text.replace(/\n/g, '<br>');
            return text;
        }
        
        async function sendMessage() {
            const text = messageInput.value.trim();
            if (!text) return;
            
            // Add user message
            addMessage(text, true);
            messageInput.value = '';
            messageInput.style.height = 'auto';
            
            // Show typing indicator
            typingIndicator.classList.add('active');
            sendButton.disabled = true;
            
            try {
                const response = await fetch(`${API_URL}/run`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ text: text })
                });
                
                const data = await response.json();
                
                // Hide typing indicator
                typingIndicator.classList.remove('active');
                sendButton.disabled = false;
                
                if (data.ok) {
                    let reply = data.plan.say || "Task completed.";
                    
                    // Add action results if any
                    if (data.exec && data.exec.action_results && data.exec.action_results.length > 0) {
                        reply += "\n\n**Actions executed:**\n";
                        data.exec.action_results.forEach(result => {
                            const icon = result.result.ok ? '[OK]' : '[FAIL]';
                            const output = result.result.output || JSON.stringify(result.result);
                            reply += `${icon} ${result.tool}.${result.op}: ${output}\n`;
                        });
                    }
                    
                    addMessage(reply, false);
                } else {
                    addMessage('Sorry, something went wrong. Please try again.', false);
                }
            } catch (error) {
                typingIndicator.classList.remove('active');
                sendButton.disabled = false;
                addMessage(`Error: ${error.message}. Make sure the AUREON server is running.`, false);
            }
        }
        
        // Check server status on load
        async function checkStatus() {
            try {
                const response = await fetch(`${API_URL}/status`);
                const data = await response.json();
                
                document.getElementById('brainStatus').textContent = 
                    `Brain: ${data.mode === 'online' ? 'Online' : 'Offline'}`;
                
                const capabilities = [];
                if (data.openai === 'ok') capabilities.push('OpenAI');
                if (data.deepseek === 'ok') capabilities.push('DeepSeek');
                
                document.getElementById('capabilityStatus').textContent = 
                    capabilities.length > 0 ? capabilities.join(' + ') : 'Limited Mode';
                    
            } catch (error) {
                document.getElementById('brainStatus').textContent = 'Brain: Connecting...';
                document.getElementById('capabilityStatus').textContent = 'Starting up...';
            }
        }
        
        checkStatus();
        setInterval(checkStatus, 30000); // Check every 30 seconds
    </script>
</body>
</html>"""
    
    html_path.write_text(html_content, encoding='utf-8')
    return html_path


if __name__ == "__main__":
    path = build_chat_interface()
    print(f"[OK] Web interface built: {path}")
    print(f"   Open in browser: file:///{path}")
