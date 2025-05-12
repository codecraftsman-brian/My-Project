import React, { useState } from 'react';
import { 
  Box, 
  Paper, 
  Typography, 
  TextField, 
  Button, 
  Container, 
  Link, 
  Tabs, 
  Tab, 
  CircularProgress, 
  Snackbar, 
  Alert 
} from '@mui/material';
import { colors } from '../styles/theme';
import axios from 'axios';

const Login = ({ onLogin }) => {
  const [activeTab, setActiveTab] = useState(0);
  const [formData, setFormData] = useState({
    login: {
      username_or_email: '',
      password: ''
    },
    register: {
      username: '',
      email: '',
      password: '',
      confirmPassword: ''
    }
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [snackbar, setSnackbar] = useState({
    open: false,
    message: '',
    severity: 'success'
  });
  
  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
    setError(null);
  };
  
  const handleInputChange = (e, formType) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [formType]: {
        ...formData[formType],
        [name]: value
      }
    });
  };
  
  const handleLogin = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    
    try {
      const response = await axios.post('/api/auth/login', {
        username_or_email: formData.login.username_or_email,
        password: formData.login.password
      });
      
      // Store token in localStorage
      localStorage.setItem('token', response.data.access_token);
      
      // Call the login callback
      if (onLogin) {
        onLogin(response.data.access_token, response.data.user);
      }
      
      setLoading(false);
    } catch (err) {
      setLoading(false);
      setError(err.response?.data?.error || 'An error occurred during login');
    }
  };
  
  const handleRegister = async (e) => {
    e.preventDefault();
    setError(null);
    
    // Validate passwords match
    if (formData.register.password !== formData.register.confirmPassword) {
      setError('Passwords do not match');
      return;
    }
    
    setLoading(true);
    
    try {
      await axios.post('/api/auth/register', {
        username: formData.register.username,
        email: formData.register.email,
        password: formData.register.password
      });
      
      // Show success message
      setSnackbar({
        open: true,
        message: 'Registration successful! Please login.',
        severity: 'success'
      });
      
      // Switch to login tab
      setActiveTab(0);
      
      // Clear register form
      setFormData({
        ...formData,
        register: {
          username: '',
          email: '',
          password: '',
          confirmPassword: ''
        }
      });
      
      setLoading(false);
    } catch (err) {
      setLoading(false);
      setError(err.response?.data?.error || 'An error occurred during registration');
    }
  };
  
  const handleCloseSnackbar = () => {
    setSnackbar({
      ...snackbar,
      open: false
    });
  };
  
  return (
    <Container maxWidth="sm" sx={{ mt: 8 }}>
      <Paper sx={{ p: 4, borderRadius: 3, boxShadow: 3 }}>
        <Box sx={{ textAlign: 'center', mb: 3 }}>
          <Typography variant="h4" component="h1" sx={{ fontWeight: 'bold', color: colors.black }}>
            TikTok Scheduler
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Schedule and manage your TikTok posts efficiently
          </Typography>
        </Box>
        
        <Tabs 
          value={activeTab} 
          onChange={handleTabChange} 
          variant="fullWidth" 
          sx={{ mb: 3, borderBottom: 1, borderColor: 'divider' }}
        >
          <Tab label="Login" />
          <Tab label="Register" />
        </Tabs>
        
        {/* Login Form */}
        {activeTab === 0 && (
          <Box component="form" onSubmit={handleLogin}>
            <TextField
              label="Username or Email"
              name="username_or_email"
              value={formData.login.username_or_email}
              onChange={(e) => handleInputChange(e, 'login')}
              fullWidth
              margin="normal"
              required
            />
            <TextField
              label="Password"
              name="password"
              type="password"
              value={formData.login.password}
              onChange={(e) => handleInputChange(e, 'login')}
              fullWidth
              margin="normal"
              required
            />
            
            {error && (
              <Typography color="error" sx={{ mt: 2 }}>
                {error}
              </Typography>
            )}
            
            <Button 
              type="submit" 
              variant="contained" 
              fullWidth 
              sx={{ mt: 3, mb: 2, py: 1, bgcolor: colors.brightRed, '&:hover': { bgcolor: colors.mediumRed } }}
              disabled={loading}
            >
              {loading ? <CircularProgress size={24} color="inherit" /> : 'Login'}
            </Button>
            
            <Typography variant="body2" align="center">
              <Link href="#" onClick={(e) => { e.preventDefault(); setActiveTab(1); }}>
                Don't have an account? Register
              </Link>
            </Typography>
          </Box>
        )}
        
        {/* Register Form */}
        {activeTab === 1 && (
          <Box component="form" onSubmit={handleRegister}>
            <TextField
              label="Username"
              name="username"
              value={formData.register.username}
              onChange={(e) => handleInputChange(e, 'register')}
              fullWidth
              margin="normal"
              required
            />
            <TextField
              label="Email"
              name="email"
              type="email"
              value={formData.register.email}
              onChange={(e) => handleInputChange(e, 'register')}
              fullWidth
              margin="normal"
              required
            />
            <TextField
              label="Password"
              name="password"
              type="password"
              value={formData.register.password}
              onChange={(e) => handleInputChange(e, 'register')}
              fullWidth
              margin="normal"
              required
            />
            <TextField
              label="Confirm Password"
              name="confirmPassword"
              type="password"
              value={formData.register.confirmPassword}
              onChange={(e) => handleInputChange(e, 'register')}
              fullWidth
              margin="normal"
              required
              error={formData.register.password !== formData.register.confirmPassword && formData.register.confirmPassword !== ''}
              helperText={formData.register.password !== formData.register.confirmPassword && formData.register.confirmPassword !== '' ? 'Passwords do not match' : ''}
            />
            
            {error && (
              <Typography color="error" sx={{ mt: 2 }}>
                {error}
              </Typography>
            )}
            
            <Button 
              type="submit" 
              variant="contained" 
              fullWidth 
              sx={{ mt: 3, mb: 2, py: 1, bgcolor: colors.brightRed, '&:hover': { bgcolor: colors.mediumRed } }}
              disabled={loading}
            >
              {loading ? <CircularProgress size={24} color="inherit" /> : 'Register'}
            </Button>
            
            <Typography variant="body2" align="center">
              <Link href="#" onClick={(e) => { e.preventDefault(); setActiveTab(0); }}>
                Already have an account? Login
              </Link>
            </Typography>
          </Box>
        )}
      </Paper>
      
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
    </Container>
  );
};

export default Login;