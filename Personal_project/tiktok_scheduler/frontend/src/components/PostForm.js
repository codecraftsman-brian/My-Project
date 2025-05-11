import React, { useState, useEffect } from 'react';
import { 
  Box, 
  Paper, 
  Typography, 
  TextField, 
  Button, 
  Grid, 
  FormControl, 
  InputLabel, 
  Select, 
  MenuItem, 
  CircularProgress,
  Snackbar,
  Alert
} from '@mui/material';
import {
  CloudUpload as CloudUploadIcon,
  Schedule as ScheduleIcon,
  Save as SaveIcon
} from '@mui/icons-material';
import { colors } from '../styles/theme';
import axios from 'axios';
import { styled } from '@mui/material/styles';

const UploadBox = styled(Box)(({ theme }) => ({
  border: `2px dashed ${colors.mediumRed}`,
  borderRadius: '8px',
  padding: theme.spacing(3),
  backgroundColor: 'rgba(255, 0, 0, 0.02)',
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  justifyContent: 'center',
  cursor: 'pointer',
  transition: 'all 0.2s ease',
  minHeight: '200px',
  '&:hover': {
    backgroundColor: 'rgba(255, 0, 0, 0.05)',
  },
}));

const VideoPreview = styled('video')({
  maxWidth: '100%',
  maxHeight: '400px',
  borderRadius: '8px',
  marginBottom: '16px',
});

const PostForm = ({ accounts, onPostCreated }) => {
  const [formData, setFormData] = useState({
    accountId: '',
    caption: '',
    scheduledTime: '',
    video: null
  });
  
  const [videoPreview, setVideoPreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [snackbar, setSnackbar] = useState({
    open: false,
    message: '',
    severity: 'success'
  });
  
  useEffect(() => {
    // Initialize with the first account if available
    if (accounts && accounts.length > 0) {
      setFormData(prev => ({
        ...prev,
        accountId: accounts[0].id
      }));
    }
    
    // Initialize scheduled time to tomorrow at noon
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    tomorrow.setHours(12, 0, 0, 0);
    
    setFormData(prev => ({
      ...prev,
      scheduledTime: tomorrow.toISOString().slice(0, 16)
    }));
  }, [accounts]);
  
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };
  
  const handleVideoChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setFormData({
        ...formData,
        video: file
      });
      
      // Create a preview
      const url = URL.createObjectURL(file);
      setVideoPreview(url);
    }
  };
  
  const handleVideoUploadClick = () => {
    // Trigger the hidden file input
    document.getElementById('video-upload').click();
  };
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.accountId || !formData.scheduledTime || !formData.video) {
      showSnackbar('Please fill in all required fields and upload a video', 'error');
      return;
    }
    
    try {
      setLoading(true);
      
      const formPayload = new FormData();
      formPayload.append('account_id', formData.accountId);
      formPayload.append('scheduled_time', formData.scheduledTime);
      formPayload.append('caption', formData.caption);
      formPayload.append('video', formData.video);
      
      await axios.post('/api/scheduler/schedule', formPayload, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
          'Content-Type': 'multipart/form-data'
        }
      });
      
      // Reset form
      setFormData({
        accountId: accounts[0]?.id || '',
        caption: '',
        scheduledTime: formData.scheduledTime,
        video: null
      });
      setVideoPreview(null);
      
      // Callback to parent component
      if (onPostCreated) {
        onPostCreated();
      }
      
      setLoading(false);
      showSnackbar('Post scheduled successfully', 'success');
      
    } catch (error) {
      console.error('Error scheduling post:', error);
      setLoading(false);
      showSnackbar(`Error scheduling post: ${error.response?.data?.error || error.message}`, 'error');
    }
  };
  
  const showSnackbar = (message, severity) => {
    setSnackbar({
      open: true,
      message,
      severity
    });
  };
  
  const handleCloseSnackbar = () => {
    setSnackbar({
      ...snackbar,
      open: false
    });
  };
  
  return (
    <Paper sx={{ p: 3 }}>
      <Typography variant="h5" sx={{ mb: 3, fontWeight: 'bold' }}>
        Create New TikTok Post
      </Typography>
      
      <form onSubmit={handleSubmit}>
        <Grid container spacing={3}>
          {/* Video Upload */}
          <Grid item xs={12} md={6}>
            <Box sx={{ mb: 3 }}>
              <Typography variant="subtitle1" sx={{ mb: 1, fontWeight: 'bold' }}>
                Upload Video*
              </Typography>
              
              <input
                id="video-upload"
                type="file"
                accept="video/mp4,video/mov,video/avi"
                onChange={handleVideoChange}
                style={{ display: 'none' }}
              />
              
              {videoPreview ? (
                <Box sx={{ textAlign: 'center' }}>
                  <VideoPreview controls src={videoPreview} />
                  <Button 
                    variant="outlined" 
                    color="primary" 
                    startIcon={<CloudUploadIcon />}
                    onClick={handleVideoUploadClick}
                  >
                    Change Video
                  </Button>
                </Box>
              ) : (
                <UploadBox onClick={handleVideoUploadClick}>
                  <CloudUploadIcon sx={{ fontSize: 48, color: colors.mediumRed, mb: 2 }} />
                  <Typography variant="body1" sx={{ textAlign: 'center', color: colors.mediumRed, mb: 1 }}>
                    Click to upload your TikTok video
                  </Typography>
                  <Typography variant="caption" sx={{ textAlign: 'center', color: 'text.secondary' }}>
                    Supported formats: MP4, MOV, AVI
                  </Typography>
                </UploadBox>
              )}
            </Box>
          </Grid>
          
          {/* Form Fields */}
          <Grid item xs={12} md={6}>
            <Box sx={{ mb: 3 }}>
              <FormControl fullWidth sx={{ mb: 3 }} required>
                <InputLabel id="account-select-label">TikTok Account</InputLabel>
                <Select
                  labelId="account-select-label"
                  name="accountId"
                  value={formData.accountId}
                  onChange={handleInputChange}
                  label="TikTok Account"
                >
                  {accounts && accounts.map((account) => (
                    <MenuItem key={account.id} value={account.id}>
                      {account.account_name} ({account.tiktok_username})
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
              
              <TextField
                label="Caption"
                name="caption"
                value={formData.caption}
                onChange={handleInputChange}
                fullWidth
                multiline
                rows={4}
                placeholder="Write your TikTok caption here..."
                sx={{ mb: 3 }}
              />
              
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
                <ScheduleIcon sx={{ mr: 1, color: colors.brightRed }} />
                <Typography variant="subtitle1" sx={{ fontWeight: 'bold' }}>
                  Schedule Time*
                </Typography>
              </Box>
              
              <TextField
                label="Schedule Time"
                type="datetime-local"
                name="scheduledTime"
                value={formData.scheduledTime}
                onChange={handleInputChange}
                fullWidth
                required
                InputLabelProps={{
                  shrink: true,
                }}
              />
            </Box>
            
            <Button 
              variant="contained" 
              color="primary" 
              fullWidth 
              type="submit"
              disabled={loading || !formData.accountId || !formData.scheduledTime || !formData.video}
              startIcon={loading ? <CircularProgress size={20} color="inherit" /> : <SaveIcon />}
              sx={{ mt: 2, py: 1.5 }}
            >
              {loading ? 'Scheduling...' : 'Schedule Post'}
            </Button>
          </Grid>
        </Grid>
      </form>
      
      {/* Snackbar for notifications */}
      <Snackbar
        open={snackbar.open}
        autoHideDuration={6000}
        onClose={handleCloseSnackbar}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
      >
        <Alert onClose={handleCloseSnackbar} severity={snackbar.severity} sx={{ width: '100%' }}>
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Paper>
  );
};

export default PostForm;