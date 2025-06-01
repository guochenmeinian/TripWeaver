import React, { useState, useRef, useEffect } from 'react';
import { 
  Container, 
  TextField, 
  Button, 
  Box, 
  Paper, 
  Typography,
  Divider
} from '@mui/material';
import Grid from '@mui/material/Grid';
import SendIcon from '@mui/icons-material/Send';
import { ChatMessage } from './components/ChatMessage';
import { ProfileViewer } from './components/ProfileViewer';
import axios from 'axios';

interface Message {
  id: number;
  text: string;
  isUser: boolean;
  timestamp: string;
}

const App: React.FC = () => {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [profile, setProfile] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // 初始化加载用户资料
  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await axios.get('api/profile');
        setProfile(response.data);
      } catch (error) {
        console.error('Error fetching profile:', error);
      }
    };
    fetchProfile();
  }, []);

  // 自动滚动到最新消息
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;

    // 添加用户消息
    const userMessage: Message = {
      id: Date.now(),
      text: input,
      isUser: true,
      timestamp: new Date().toISOString(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      // 发送消息到后端
      const response = await axios.post('api/chat', { message: input });
      
      // 添加AI回复
      const aiMessage: Message = {
        id: Date.now() + 1,
        text: response.data.reply,
        isUser: false,
        timestamp: new Date().toISOString(),
      };

      setMessages(prev => [...prev, aiMessage]);
      
      // 更新资料（如果需要）
      if (response.data.profile) {
        setProfile(response.data.profile);
      }
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage: Message = {
        id: Date.now() + 1,
        text: 'Sorry, there was an error processing your request.',
        isUser: false,
        timestamp: new Date().toISOString(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <Container maxWidth="lg" sx={{ py: 4, height: '100vh', display: 'flex', flexDirection: 'column' }}>
      <Typography variant="h4" component="h1" gutterBottom align="center" sx={{ mb: 4 }}>
        TripWeaver Travel Assistant
      </Typography>
      
      <Grid container spacing={3} sx={{ flex: 1, overflow: 'hidden' }}>
        <Grid item xs={12} md={8} sx={{ display: 'flex', flexDirection: 'column' }}>
          <Paper 
            elevation={3} 
            sx={{ 
              p: 2, 
              flex: 1, 
              display: 'flex', 
              flexDirection: 'column',
              overflow: 'hidden'
            }}
          >
            <Box sx={{ flex: 1, overflowY: 'auto', mb: 2, p: 1 }}>
              {messages.length === 0 ? (
                <Box 
                  sx={{ 
                    display: 'flex', 
                    justifyContent: 'center', 
                    alignItems: 'center', 
                    height: '100%',
                    color: 'text.secondary'
                  }}
                >
                  <Typography>Start a conversation with TripWeaver...</Typography>
                </Box>
              ) : (
                messages.map((msg) => (
                  <ChatMessage
                    key={msg.id}
                    message={msg.text}
                    isUser={msg.isUser}
                    timestamp={msg.timestamp}
                  />
                ))
              )}
              <div ref={messagesEndRef} />
            </Box>
            
            <Divider sx={{ my: 2 }} />
            
            <Box sx={{ display: 'flex', gap: 1 }}>
              <TextField
                fullWidth
                variant="outlined"
                placeholder="Type your message here..."
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={handleKeyPress}
                disabled={isLoading}
                multiline
                maxRows={4}
              />
              <Button
                variant="contained"
                color="primary"
                onClick={handleSend}
                disabled={isLoading || !input.trim()}
                sx={{ minWidth: '100px' }}
                endIcon={<SendIcon />}
              >
                {isLoading ? 'Sending...' : 'Send'}
              </Button>
            </Box>
          </Paper>
        </Grid>
        
        {/* 个人资料区域 */}
        <Grid item xs={12} md={4} sx={{ display: 'flex', flexDirection: 'column' }}>
          {profile ? (
            <ProfileViewer profile={profile} />
          ) : (
            <Paper 
              elevation={3} 
              sx={{ 
                p: 3, 
                height: '100%',
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center'
              }}
            >
              <Typography>Loading profile...</Typography>
            </Paper>
          )}
        </Grid>
      </Grid>
    </Container>
  );
};

export default App;