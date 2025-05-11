import React, { useState, useEffect } from 'react';
import { 
  Box, 
  Paper, 
  Typography, 
  Divider, 
  Switch, 
  FormControlLabel, 
  TextField, 
  Button, 
  Grid, 
  InputAdornment, 
  IconButton,
  Card,
  CardContent,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  CircularProgress,
  Snackbar,
  Alert
} from '@mui/material';
import { 
  Visibility as VisibilityIcon, 
  VisibilityOff as VisibilityOffIcon,
  ExpandMore as ExpandMoreIcon,
  Security as SecurityIcon,
  Notifications as NotificationsIcon,
  Schedule as ScheduleIcon,
  AccountCircle as AccountCircleIcon,
  Help as HelpIcon
} from '@mui/icons-material';
import { colors } from '../styles/theme';
import axios from 'axios';

const Settings = () => {
  // User settings state
  const [settings, setSettings] = useState({
    enableEmailNotifications: true,
    notifyOnSuccess: true,
    notifyOnFailure: true,
    defaultScheduleTime: '12:00',
    encryptionEnabled: true,
    darkMode: false,
    autoRefreshTokens: true
  });
  
  // Password change state
  const [passwordForm, setPasswordForm] = useState({
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
  });
  
  // Profile state
  const [profile, setProfile] = useState({
    username: '',
    email: ''
  });
  
  // UI state
  const [showCurrentPassword, setShowCurrentPassword] = useState(false);
  const [showNewPassword, setShowNewPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [openDeleteDialog, setOpenDeleteDialog] = useState(false);
  const [deleteConfirmPassword, setDeleteConfirmPassword] = useState('');
  const [snackbar, setSnackbar] = useState({
    open: false,
    message: '',
    severity: 'success'
  });
  
  // Fetch user data and settings
  useEffect(() => {
    fetchUserData();
  }, []);
  
  const fetchUserData = async () => {
    try {
      setLoading(true);
      
      // In a real app, you would fetch from your API
      const response = await axios.get('/api/auth/user', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      
      // Set profile data
      setProfile({
        username: response.data.username,
        email: response.data.email
      });
      
      // In a real app, you would also fetch user settings
      // For now, we'll use the default values
      
      setLoading(false);
    } catch (error) {
      console.error('Error fetching user data:', error);
      setLoading(false);
      showSnackbar('Failed to load user data', 'error');
    }
  };
  
  const handleSettingChange = (setting) => (event) => {
    setSettings({
      ...settings,
      [setting]: event.target.checked
    });
    
    // In a real app, you would save this to your API
    showSnackbar('Settings saved', 'success');
  };
  
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    
    if (name === 'deleteConfirmPassword') {
      setDeleteConfirmPassword(value);
    } else if (name.startsWith('password')) {
      setPasswordForm({
        ...passwordForm,
        [name.replace('password', '')]: value
      });
    } else {
      setProfile({
        ...profile,
        [name]: value
      });
    }
  };
  
  const handleSaveProfile = async () => {
    try {
      setLoading(true);
      
      // In a real app, you would update the profile via API
      await new Promise(resolve => setTimeout(resolve, 500)); // Simulate API call
      
      setLoading(false);
      showSnackbar('Profile updated successfully', 'success');
    } catch (error) {
      console.error('Error updating profile:', error);
      setLoading(false);
      showSnackbar('Failed to update profile', 'error');
    }
  };
  
  const handleChangePassword = async () => {
    // Validate passwords
    if (passwordForm.newPassword !== passwordForm.confirmPassword) {
      showSnackbar('New passwords do not match', 'error');
      return;
    }
    
    if (passwordForm.newPassword.length < 8) {
      showSnackbar('Password must be at least 8 characters long', 'error');
      return;
    }
    
    try {
      setLoading(true);
      
      // In a real app, you would change the password via API
      await axios.post('/api/auth/change-password', {
        current_password: passwordForm.currentPassword,
        new_password: passwordForm.newPassword
      }, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      
      // Reset form
      setPasswordForm({
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
      });
      
      setLoading(false);
      showSnackbar('Password changed successfully', 'success');
    } catch (error) {
      console.error('Error changing password:', error);
      setLoading(false);
      showSnackbar(error.response?.data?.error || 'Failed to change password', 'error');
    }
  };
  
  const handleOpenDeleteDialog = () => {
    setOpenDeleteDialog(true);
    setDeleteConfirmPassword('');
  };
  
  const handleCloseDeleteDialog = () => {
    setOpenDeleteDialog(false);
  };
  
  const handleDeleteAccount = async () => {
    try {
      setLoading(true);
      
      // In a real app, you would delete the account via API
      await axios.post('/api/auth/delete-account', {
        password: deleteConfirmPassword
      }, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      
      setLoading(false);
      handleCloseDeleteDialog();
      
      // In a real app, you would log the user out and redirect them
      localStorage.removeItem('token');
      window.location.href = '/login';
      
    } catch (error) {
      console.error('Error deleting account:', error);
      setLoading(false);
      showSnackbar(error.response?.data?.error || 'Failed to delete account', 'error');
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
  
  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '400px' }}>
        <CircularProgress sx={{ color: colors.brightRed }} />
      </Box>
    );
  }
  
  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" component="h1" sx={{ mb: 4, fontWeight: 'bold' }}>
        Settings
      </Typography>
      
      {/* User Profile */}
      <Accordion defaultExpanded sx={{ mb: 3 }}>
        <AccordionSummary
          expandIcon={<ExpandMoreIcon />}
          sx={{ bgcolor: colors.black, color: 'white' }}
        >
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <AccountCircleIcon sx={{ mr: 1 }} />
            <Typography variant="h6">Account Profile</Typography>
          </Box>
        </AccordionSummary>
        <AccordionDetails>
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <TextField
                label="Username"
                name="username"
                value={profile.username}
                onChange={handleInputChange}
                fullWidth
                margin="normal"
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                label="Email"
                name="email"
                value={profile.email}
                onChange={handleInputChange}
                fullWidth
                margin="normal"
                type="email"
              />
            </Grid>
            <Grid item xs={12} sx={{ display: 'flex', justifyContent: 'flex-end' }}>
              <Button 
                variant="contained" 
                color="primary"
                onClick={handleSaveProfile}
              >
                Save Profile
              </Button>
            </Grid>
          </Grid>
        </AccordionDetails>
      </Accordion>
      
      {/* Security */}
      <Accordion sx={{ mb: 3 }}>
        <AccordionSummary
          expandIcon={<ExpandMoreIcon />}
          sx={{ bgcolor: colors.darkRed, color: 'white' }}
        >
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <SecurityIcon sx={{ mr: 1 }} />
            <Typography variant="h6">Security</Typography>
          </Box>
        </AccordionSummary>
        <AccordionDetails>
          <Typography variant="h6" sx={{ mb: 2 }}>Change Password</Typography>
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <TextField
                label="Current Password"
                name="passwordcurrentPassword"
                value={passwordForm.currentPassword}
                onChange={handleInputChange}
                fullWidth
                margin="normal"
                type={showCurrentPassword ? 'text' : 'password'}
                InputProps={{
                  endAdornment: (
                    <InputAdornment position="end">
                      <IconButton
                        onClick={() => setShowCurrentPassword(!showCurrentPassword)}
                        edge="end"
                      >
                        {showCurrentPassword ? <VisibilityOffIcon /> : <VisibilityIcon />}
                      </IconButton>
                    </InputAdornment>
                  )
                }}
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                label="New Password"
                name="passwordnewPassword"
                value={passwordForm.newPassword}
                onChange={handleInputChange}
                fullWidth
                margin="normal"
                type={showNewPassword ? 'text' : 'password'}
                InputProps={{
                  endAdornment: (
                    <InputAdornment position="end">
                      <IconButton
                        onClick={() => setShowNewPassword(!showNewPassword)}
                        edge="end"
                      >
                        {showNewPassword ? <VisibilityOffIcon /> : <VisibilityIcon />}
                      </IconButton>
                    </InputAdornment>
                  )
                }}
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                label="Confirm New Password"
                name="passwordconfirmPassword"
                value={passwordForm.confirmPassword}
                onChange={handleInputChange}
                fullWidth
                margin="normal"
                type="password"
                error={passwordForm.newPassword !== passwordForm.confirmPassword && passwordForm.confirmPassword !== ''}
                helperText={passwordForm.newPassword !== passwordForm.confirmPassword && passwordForm.confirmPassword !== '' ? 'Passwords do not match' : ''}
              />
            </Grid>
            <Grid item xs={12} sx={{ display: 'flex', justifyContent: 'flex-end' }}>
              <Button 
                variant="contained" 
                color="primary"
                onClick={handleChangePassword}
                disabled={!passwordForm.currentPassword || !passwordForm.newPassword || !passwordForm.confirmPassword || passwordForm.newPassword !== passwordForm.confirmPassword}
              >
                Change Password
              </Button>
            </Grid>
          </Grid>
          
          <Divider sx={{ my: 3 }} />
          
          <FormControlLabel
            control={
              <Switch
                checked={settings.encryptionEnabled}
                onChange={handleSettingChange('encryptionEnabled')}
                color="primary"
              />
            }
            label="Enable Client-Side Encryption"
          />
          <Typography variant="body2" color="text.secondary" sx={{ mt: 1, ml: 1 }}>
            Enable additional encryption for your TikTok API tokens
          </Typography>
        </AccordionDetails>
      </Accordion>
      
      {/* Notifications */}
      <Accordion sx={{ mb: 3 }}>
        <AccordionSummary
          expandIcon={<ExpandMoreIcon />}
          sx={{ bgcolor: colors.mediumRed, color: 'white' }}
        >
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <NotificationsIcon sx={{ mr: 1 }} />
            <Typography variant="h6">Notifications</Typography>
          </Box>
        </AccordionSummary>
        <AccordionDetails>
          <FormControlLabel
            control={
              <Switch
                checked={settings.enableEmailNotifications}
                onChange={handleSettingChange('enableEmailNotifications')}
                color="primary"
              />
            }
            label="Email Notifications"
          />
          
          <Box sx={{ ml: 4, mt: 1 }}>
            <FormControlLabel
              control={
                <Switch
                  checked={settings.notifyOnSuccess}
                  onChange={handleSettingChange('notifyOnSuccess')}
                  color="primary"
                  disabled={!settings.enableEmailNotifications}
                />
              }
              label="Notify on successful posts"
            />
            
            <FormControlLabel
              control={
                <Switch
                  checked={settings.notifyOnFailure}
                  onChange={handleSettingChange('notifyOnFailure')}
                  color="primary"
                  disabled={!settings.enableEmailNotifications}
                />
              }
              label="Notify on failed posts"
            />
          </Box>
        </AccordionDetails>
      </Accordion>
      
      {/* Scheduling */}
      <Accordion sx={{ mb: 3 }}>
        <AccordionSummary
          expandIcon={<ExpandMoreIcon />}
          sx={{ bgcolor: colors.brightRed, color: 'white' }}
        >
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <ScheduleIcon sx={{ mr: 1 }} />
            <Typography variant="h6">Scheduling Preferences</Typography>
          </Box>
        </AccordionSummary>
        <AccordionDetails>
          <Box sx={{ mb: 2 }}>
            <Typography variant="subtitle1" sx={{ mb: 1 }}>Default Scheduling Time</Typography>
            <TextField
              type="time"
              value={settings.defaultScheduleTime}
              onChange={(e) => setSettings({ ...settings, defaultScheduleTime: e.target.value })}
              InputLabelProps={{
                shrink: true,
              }}
              inputProps={{
                step: 300, // 5 min
              }}
              sx={{ width: 200 }}
            />
          </Box>
          
          <FormControlLabel
            control={
              <Switch
                checked={settings.autoRefreshTokens}
                onChange={handleSettingChange('autoRefreshTokens')}
                color="primary"
              />
            }
            label="Automatically refresh TikTok API tokens before they expire"
          />
        </AccordionDetails>
      </Accordion>
      
      {/* Account Deletion */}
      <Card sx={{ mb: 3, bgcolor: '#fff8f8', border: '1px solid #ffcccc' }}>
        <CardContent>
          <Typography variant="h6" color="error" sx={{ mb: 2 }}>
            Delete Account
          </Typography>
          <Typography variant="body2" sx={{ mb: 2 }}>
            This action is permanent and cannot be undone. All your data, including accounts, scheduled posts, and settings will be permanently deleted.
          </Typography>
          <Button 
            variant="outlined" 
            color="error"
            onClick={handleOpenDeleteDialog}
          >
            Delete My Account
          </Button>
        </CardContent>
      </Card>
      
      {/* Delete Account Dialog */}
      <Dialog
        open={openDeleteDialog}
        onClose={handleCloseDeleteDialog}
        PaperProps={{
          sx: {
            borderRadius: '12px'
          }
        }}
      >
        <DialogTitle sx={{ bgcolor: 'error.main', color: 'white' }}>
          Confirm Account Deletion
        </DialogTitle>
        <DialogContent sx={{ mt: 2 }}>
          <Typography variant="body1" sx={{ mb: 2 }}>
            Please enter your password to confirm that you want to permanently delete your account.
          </Typography>
          <TextField
            label="Password"
            name="deleteConfirmPassword"
            value={deleteConfirmPassword}
            onChange={handleInputChange}
            fullWidth
            margin="normal"
            type="password"
          />
        </DialogContent>
        <DialogActions sx={{ p: 2 }}>
          <Button onClick={handleCloseDeleteDialog} color="inherit">
            Cancel
          </Button>
          <Button 
            onClick={handleDeleteAccount} 
            variant="contained" 
            color="error"
            disabled={!deleteConfirmPassword}
          >
            Delete My Account
          </Button>
        </DialogActions>
      </Dialog>
      
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
    </Box>
  );
};

export default Settings;