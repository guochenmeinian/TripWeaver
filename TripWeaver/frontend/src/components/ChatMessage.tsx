// src/components/ChatMessage.tsx
import { Paper, PaperProps, styled, Box, Typography, Avatar } from '@mui/material';

interface StyledMessageProps extends PaperProps {
  isUser: boolean;
}

const StyledMessage = styled(Paper, {
  shouldForwardProp: (prop) => prop !== 'isUser',
})<StyledMessageProps>(({ theme, isUser }) => ({
  maxWidth: '70%',
  padding: theme.spacing(1.5),
  marginBottom: theme.spacing(1),
  marginLeft: isUser ? 'auto' : theme.spacing(1),
  marginRight: isUser ? theme.spacing(1) : 'auto',
  backgroundColor: isUser ? '#e3f2fd' : '#f5f5f5',
  borderRadius: '12px',
}));

export const ChatMessage: React.FC<{
  message: string;
  isUser: boolean;
  timestamp: string;
}> = ({ message, isUser, timestamp }) => {
  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: isUser ? 'flex-end' : 'flex-start',
        mb: 2,
      }}
    >
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 0.5 }}>
        {!isUser && <Avatar sx={{ bgcolor: '#1976d2', mr: 1 }}>AI</Avatar>}
        <Typography variant="caption" color="text.secondary">
          {isUser ? 'You' : 'TripWeaver'} • {new Date(timestamp).toLocaleTimeString()}
        </Typography>
      </Box>
      <StyledMessage elevation={1} isUser={isUser}>
        <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap' }}>
          {message}
        </Typography>
      </StyledMessage>
    </Box>
  );
};