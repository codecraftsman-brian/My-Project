import React, { useState, useEffect } from 'react';
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

export default Calendar;