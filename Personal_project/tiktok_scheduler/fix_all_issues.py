#!/usr/bin/env python3
"""
A script to fix all the identified issues with the TikTok Scheduler application.
"""

import os
import shutil
import re
import sys

def create_directory_if_missing(directory):
    """Create directory if it doesn't exist"""
    if not os.path.exists(directory):
        print(f"Creating directory: {directory}")
        os.makedirs(directory, exist_ok=True)
    else:
        print(f"Directory exists: {directory}")

def create_calendar_js():
    """Create the Calendar.js file"""
    file_path = "frontend/src/components/Calendar.js"
    calendar_content = """import React, { useState, useEffect } from 'react';
import { 
  Box, 
  Paper, 
  Typography, 
  Grid, 
  Button, 
  Dialog, 
  DialogTitle, 
  DialogContent, 
  DialogActions,
  IconButton,
  TextField,
  MenuItem,
  FormControl,
  InputLabel,
  Select,
  CircularProgress
} from '@mui/material';
import { styled } from '@mui/material/styles';
import { 
  ChevronLeft as ChevronLeftIcon, 
  ChevronRight as ChevronRightIcon,
  Close as CloseIcon,
  Upload as UploadIcon
} from '@mui/icons-material';
import { colors } from '../styles/theme';
import { format, startOfMonth, endOfMonth, eachDayOfInterval, getDay, addMonths, subMonths, isSameDay } from 'date-fns';
import axios from 'axios';

// Styled components
const StyledDay = styled(Paper)(({ theme, isToday, hasPost, isCurrentMonth }) => ({
  height: '100px',
  padding: theme.spacing(1),
  display: 'flex',
  flexDirection: 'column',
  backgroundColor: isToday ? 'rgba(255, 0, 0, 0.05)' : (isCurrentMonth ? 'white' : '#f9f9f9'),
  cursor: 'pointer',
  border: isToday ? `1px solid ${colors.brightRed}` : '1px solid transparent',
  transition: 'all 0.2s ease',
  '&:hover': {
    transform: 'scale(1.05)',
    zIndex: 1,
    boxShadow: '0px 4px 20px rgba(0, 0, 0, 0.1)',
  },
  position: 'relative',
  overflow: 'hidden',
}));

const PostIndicator = styled('div')(({ theme, status }) => ({
  width: '10px',
  height: '10px',
  borderRadius: '50%',
  backgroundColor: 
    status === 'sent' ? 'green' : 
    status === 'scheduled' ? colors.brightRed : 
    status === 'failed' ? 'gray' : 'blue',
  margin: '2px',
  display: 'inline-block',
}));

const UploadButton = styled('label')(({ theme }) => ({
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  justifyContent: 'center',
  border: `2px dashed ${colors.mediumRed}`,
  borderRadius: '8px',
  padding: theme.spacing(3),
  backgroundColor: 'rgba(255, 0, 0, 0.02)',
  cursor: 'pointer',
  transition: 'all 0.2s ease',
  minHeight: '100px',
  '&:hover': {
    backgroundColor: 'rgba(255, 0, 0, 0.05)',
  },
}));

const VideoPreview = styled('video')({
  maxWidth: '100%',
  maxHeight: '200px',
  marginBottom: '16px',
});

const Calendar = ({ accounts }) => {
  const [currentMonth, setCurrentMonth] = useState(new Date());
  const [selectedDate, setSelectedDate] = useState(null);
  const [openDialog, setOpenDialog] = useState(false);
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(false);
  
  // Form state
  const [formData, setFormData] = useState({
    accountId: '',
    caption: '',
    scheduledTime: '',
    video: null
  });
  const [videoPreview, setVideoPreview] = useState(null);
  
  // Loading states
  const [loadingPosts, setLoadingPosts] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  
  // Fetch posts when the month changes
  useEffect(() => {
    if (accounts && accounts.length > 0) {
      fetchPosts();
    }
  }, [currentMonth, accounts]);
  
  const fetchPosts = async () => {
    try {
      setLoadingPosts(true);
      const startDate = startOfMonth(currentMonth);
      const endDate = endOfMonth(currentMonth);
      
      const response = await axios.get('/api/scheduler/posts', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      
      setPosts(response.data.posts);
      setLoadingPosts(false);
    } catch (error) {
      console.error('Error fetching posts:', error);
      setLoadingPosts(false);
    }
  };
  
  const handleNextMonth = () => {
    setCurrentMonth(addMonths(currentMonth, 1));
  };
  
  const handlePrevMonth = () => {
    setCurrentMonth(subMonths(currentMonth, 1));
  };
  
  const handleDateClick = (day) => {
    setSelectedDate(day);
    setOpenDialog(true);
    
    // Reset form
    setFormData({
      accountId: accounts && accounts.length > 0 ? accounts[0].id : '',
      caption: '',
      scheduledTime: `${format(day, 'yyyy-MM-dd')}T12:00`,
      video: null
    });
    setVideoPreview(null);
  };
  
  const handleCloseDialog = () => {
    setOpenDialog(false);
    setSelectedDate(null);
  };
  
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
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.accountId || !formData.scheduledTime || !formData.video) {
      alert('Please fill in all required fields and upload a video');
      return;
    }
    
    try {
      setSubmitting(true);
      
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
      
      // Refresh posts
      fetchPosts();
      
      // Close dialog
      handleCloseDialog();
      setSubmitting(false);
      
    } catch (error) {
      console.error('Error scheduling post:', error);
      alert(`Error scheduling post: ${error.response?.data?.error || error.message}`);
      setSubmitting(false);
    }
  };
  
  // Calendar helpers
  const monthStart = startOfMonth(currentMonth);
  const monthEnd = endOfMonth(currentMonth);
  const daysInMonth = eachDayOfInterval({ start: monthStart, end: monthEnd });
  
  // Get the day of the week for the first day of the month (0 = Sunday, 6 = Saturday)
  const startDay = getDay(monthStart);
  
  // Get posts for this month
  const postsInMonth = posts.filter(post => {
    const postDate = new Date(post.scheduled_time);
    return postDate >= monthStart && postDate <= monthEnd;
  });
  
  // Get posts for a specific day
  const getPostsForDay = (day) => {
    return postsInMonth.filter(post => {
      const postDate = new Date(post.scheduled_time);
      return isSameDay(postDate, day);
    });
  };
  
  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1" sx={{ fontWeight: 'bold' }}>
          Schedule Posts
        </Typography>
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <IconButton onClick={handlePrevMonth}>
            <ChevronLeftIcon />
          </IconButton>
          <Typography variant="h6" sx={{ mx: 2, minWidth: '150px', textAlign: 'center' }}>
            {format(currentMonth, 'MMMM yyyy')}
          </Typography>
          <IconButton onClick={handleNextMonth}>
            <ChevronRightIcon />
          </IconButton>
        </Box>
      </Box>
      
      {loadingPosts ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
          <CircularProgress sx={{ color: colors.brightRed }} />
        </Box>
      ) : (
        <>
          {/* Day headers */}
          <Grid container spacing={1} sx={{ mb: 1 }}>
            {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map((day, index) => (
              <Grid item xs key={day} sx={{ textAlign: 'center' }}>
                <Typography variant="subtitle1" fontWeight="bold">
                  {day}
                </Typography>
              </Grid>
            ))}
          </Grid>
          
          {/* Calendar grid */}
          <Grid container spacing={1}>
            {/* Empty cells for days before the start of the month */}
            {Array.from({ length: startDay }).map((_, index) => (
              <Grid item xs key={`empty-${index}`}>
                <StyledDay elevation={1} isCurrentMonth={false} />
              </Grid>
            ))}
            
            {/* Days of the month */}
            {daysInMonth.map((day, index) => {
              const dayPosts = getPostsForDay(day);
              const isToday = isSameDay(day, new Date());
              
              return (
                <Grid item xs key={index}>
                  <StyledDay 
                    elevation={1} 
                    isToday={isToday}
                    hasPost={dayPosts.length > 0}
                    isCurrentMonth={true}
                    onClick={() => handleDateClick(day)}
                  >
                    <Typography variant="subtitle1" fontWeight={isToday ? 'bold' : 'normal'}>
                      {format(day, 'd')}
                    </Typography>
                    
                    {/* Post indicators */}
                    <Box sx={{ mt: 'auto', display: 'flex', flexWrap: 'wrap' }}>
                      {dayPosts.slice(0, 3).map((post, i) => (
                        <PostIndicator key={i} status={post.status} />
                      ))}
                      {dayPosts.length > 3 && (
                        <Typography variant="caption" sx={{ ml: 1 }}>
                          +{dayPosts.length - 3} more
                        </Typography>
                      )}
                    </Box>
                  </StyledDay>
                </Grid>
              );
            })}
          </Grid>
        </>
      )}
      
      {/* Schedule post dialog */}
      <Dialog 
        open={openDialog} 
        onClose={handleCloseDialog} 
        maxWidth="md" 
        fullWidth
        PaperProps={{
          sx: {
            borderRadius: '12px'
          }
        }}
      >
        <DialogTitle sx={{ backgroundColor: colors.black, color: 'white', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Typography variant="h6">
            Schedule Post for {selectedDate ? format(selectedDate, 'MMMM d, yyyy') : ''}
          </Typography>
          <IconButton edge="end" color="inherit" onClick={handleCloseDialog}>
            <CloseIcon />
          </IconButton>
        </DialogTitle>
        
        <DialogContent dividers>
          <form onSubmit={handleSubmit}>
            <Grid container spacing={3}>
              <Grid item xs={12}>
                {videoPreview ? (
                  <Box sx={{ textAlign: 'center', my: 2 }}>
                    <VideoPreview controls src={videoPreview} />
                    <Button 
                      variant="outlined" 
                      color="primary" 
                      startIcon={<UploadIcon />}
                      component="label"
                      sx={{ mt: 1 }}
                    >
                      Change Video
                      <input
                        type="file"
                        hidden
                        accept="video/mp4,video/mov,video/avi"
                        onChange={handleVideoChange}
                      />
                    </Button>
                  </Box>
                ) : (
                  <UploadButton>
                    <input
                      type="file"
                      hidden
                      accept="video/mp4,video/mov,video/avi"
                      onChange={handleVideoChange}
                    />
                    <UploadIcon sx={{ fontSize: 40, color: colors.mediumRed, mb: 1 }} />
                    <Typography variant="body1" sx={{ textAlign: 'center', color: colors.mediumRed }}>
                      Upload TikTok Video
                    </Typography>
                    <Typography variant="caption" sx={{ textAlign: 'center', color: 'text.secondary', mt: 1 }}>
                      Supported formats: MP4, MOV, AVI
                    </Typography>
                  </UploadButton>
                )}
              </Grid>
              
              <Grid item xs={12} md={6}>
                <FormControl fullWidth required>
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
              </Grid>
              
              <Grid item xs={12} md={6}>
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
              </Grid>
              
              <Grid item xs={12}>
                <TextField
                  label="Caption"
                  name="caption"
                  value={formData.caption}
                  onChange={handleInputChange}
                  fullWidth
                  multiline
                  rows={4}
                  placeholder="Write your TikTok caption here..."
                />
              </Grid>
            </Grid>
          </form>
        </DialogContent>
        
        <DialogActions sx={{ p: 2 }}>
          <Button onClick={handleCloseDialog} color="inherit">
            Cancel
          </Button>
          <Button 
            onClick={handleSubmit} 
            variant="contained" 
            color="primary"
            disabled={!formData.accountId || !formData.scheduledTime || !formData.video || submitting}
            startIcon={submitting && <CircularProgress size={20} color="inherit" />}
          >
            {submitting ? 'Scheduling...' : 'Schedule Post'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Calendar;"""
    
    with open(file_path, 'w') as f:
        f.write(calendar_content)
    print(f"Created: {file_path}")

def create_api_js():
    """Create the api.js file"""
    file_path = "frontend/src/services/api.js"
    api_content = """import axios from 'axios';

// Create axios instance with common configuration
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:5000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle common errors
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // Handle 401 Unauthorized errors
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth endpoints
const auth = {
  register: (userData) => api.post('/auth/register', userData),
  login: (credentials) => api.post('/auth/login', credentials),
  getUser: () => api.get('/auth/user'),
  changePassword: (passwordData) => api.post('/auth/change-password', passwordData),
  deleteAccount: (password) => api.post('/auth/delete-account', { password }),
};

// Account endpoints
const accounts = {
  getAll: () => api.get('/dashboard/accounts'),
  getAuthUrl: () => api.get('/auth/tiktok-auth-url'),
  completeAuth: (code, accountName) => api.post('/accounts/complete-auth', { code, account_name: accountName }),
  update: (id, data) => api.put(`/accounts/${id}`, data),
  delete: (id) => api.delete(`/accounts/${id}`),
  refreshToken: (id) => api.post(`/accounts/${id}/refresh-token`),
};

// Scheduler endpoints
const scheduler = {
  getPosts: (filters = {}) => api.get('/scheduler/posts', { params: filters }),
  schedulePost: (formData) => api.post('/scheduler/schedule', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  }),
  reschedulePost: (id, scheduledTime) => api.put(`/scheduler/reschedule/${id}`, { scheduled_time: scheduledTime }),
  updatePost: (id, formData) => api.put(`/scheduler/update/${id}`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  }),
  cancelPost: (id) => api.delete(`/scheduler/cancel/${id}`),
};

// Dashboard endpoints
const dashboard = {
  getStats: () => api.get('/dashboard/stats'),
  getMonthlyStats: () => api.get('/dashboard/monthly-stats'),
  getFailedPosts: () => api.get('/dashboard/failed-posts'),
  getUpcomingPosts: () => api.get('/dashboard/upcoming-posts'),
};

export default {
  auth,
  accounts,
  scheduler,
  dashboard,
};"""
    
    with open(file_path, 'w') as f:
        f.write(api_content)
    print(f"Created: {file_path}")

def create_favicon():
    """Create a simple favicon.ico file"""
    file_path = "frontend/public/favicon.ico"
    # Create an empty file as a placeholder
    with open(file_path, 'wb') as f:
        f.write(b'\x00\x00\x00\x00')
    print(f"Created placeholder: {file_path}")

def create_logo():
    """Create a simple logo192.png file"""
    file_path = "frontend/public/logo192.png"
    # Create an empty file as a placeholder
    with open(file_path, 'wb') as f:
        f.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82')
    print(f"Created placeholder: {file_path}")

def fix_app_js():
    """Fix the typo in App.js"""
    file_path = "frontend/src/App.js"
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Fix the typo if found
        updated_content = content.replace('./componeents/Calendar', './components/Calendar')
        
        if content != updated_content:
            with open(file_path, 'w') as f:
                f.write(updated_content)
            print(f"Fixed typo in: {file_path}")
        else:
            print(f"No typo found in: {file_path}")
    else:
        print(f"File missing: {file_path}")

def ensure_env_file():
    """Ensure the .env file exists with SKIP_PREFLIGHT_CHECK=true"""
    file_path = "frontend/.env"
    env_content = """SKIP_PREFLIGHT_CHECK=true
REACT_APP_API_URL=http://localhost:5000/api
"""
    
    with open(file_path, 'w') as f:
        f.write(env_content)
    print(f"Created/Updated: {file_path}")

def main():
    """Main function to fix all issues"""
    print("Starting fix process...")
    
    # Create directories if missing
    create_directory_if_missing("frontend/src/components")
    create_directory_if_missing("frontend/src/services")
    create_directory_if_missing("frontend/public")
    
    # Create missing files
    create_calendar_js()
    create_api_js()
    create_favicon()
    create_logo()
    
    # Fix App.js
    fix_app_js()
    
    # Ensure .env file
    ensure_env_file()
    
    print("\nFix process completed!")
    print("Please restart your frontend server to apply the changes:")
    print("  1. Stop the current server (Ctrl+C)")
    print("  2. Start it again: cd frontend && npm start")

if __name__ == "__main__":
    main()