import React from 'react';
import { Box, Typography, Paper, Tabs, Tab } from '@mui/material';
import { JsonView, darkStyles } from 'react-json-view-lite';
import 'react-json-view-lite/dist/index.css';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`profile-tabpanel-${index}`}
      aria-labelledby={`profile-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          <Typography>{children}</Typography>
        </Box>
      )}
    </div>
  );
}

export const ProfileViewer: React.FC<{ profile: any }> = ({ profile }) => {
  const [tabValue, setTabValue] = React.useState(0);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  return (
    <Paper elevation={2} sx={{ p: 2, height: '100%' }}>
      <Tabs value={tabValue} onChange={handleTabChange} aria-label="profile tabs">
        <Tab label="User Profile" />
        <Tab label="Itinerary" />
        <Tab label="Raw JSON" />
      </Tabs>
      <TabPanel value={tabValue} index={0}>
        <Typography variant="h6" gutterBottom>User Information</Typography>
        <JsonView 
          data={profile.user_profile} 
          style={darkStyles} 
          shouldExpandNode={(level) => level < 2} 
        />
      </TabPanel>
      <TabPanel value={tabValue} index={1}>
        <Typography variant="h6" gutterBottom>Travel Itinerary</Typography>
        <JsonView 
          data={profile.itinerary} 
          style={darkStyles} 
          shouldExpandNode={(level) => level < 2} 
        />
      </TabPanel>
      <TabPanel value={tabValue} index={2}>
        <Typography variant="h6" gutterBottom>Complete Profile JSON</Typography>
        <JsonView 
          data={profile} 
          style={darkStyles} 
          shouldExpandNode={(level) => level < 1} 
        />
      </TabPanel>
    </Paper>
  );
};