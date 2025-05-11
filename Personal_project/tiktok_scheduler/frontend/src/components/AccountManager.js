import React, { useState, useEffect } from 'react';
import { 
  Box, 
  Paper, 
  Typography, 
  Button, 
  List, 
  ListItem, 
  ListItemAvatar, 
  ListItemText, 
  Avatar, 
  Divider, 
  IconButton, 
  Dialog, 
  DialogTitle, 
  DialogContent, 
  DialogActions, 
  TextField,
  CircularProgress,
  Snackbar,
  Alert,
  Chip
} from '@mui/material';
import { 
  Add as AddIcon,
  Delete as DeleteIcon,
  Edit as EditIcon,
  Person as PersonIcon,
  Refresh as RefreshIcon,
  Check as CheckIcon,
  Close as CloseIcon
} from '@mui/icons-material';
import { colors } from '../styles/theme';
import axios from 'axios';

const AccountManager = () => {
  const [accounts, setAccounts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [openDialog, setOpenDialog] = useState(false);
  const [dialogType, setDialogType] = useState('add'); // 'add', 'edit'
  const [selectedAccount, setSelectedAccount] = useState(null);
  const [formData, setFormData] = useState({
    accountName: '',
    tiktokUsername: ''
  });
  const [authUrl, setAuthUrl] = useState('');
  const [snackbar, setSnackbar] = useState({
    open: false,
    message: '',
    severity: 'success'
  });
  
  useEffect(() => {
    fetchAccounts();
  }, []);
  
  const fetchAccounts = async () => {
    try {
      setLoading(true);
      
      const response = await axios.get('/api/dashboard/accounts', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      
      setAccounts(response.data.accounts);
      setLoading(false);
      
    } catch (error) {
      console.error('Error fetching accounts:', error);
      setLoading(false);
      showSnackbar('Failed to load accounts', 'error');
    }
  };
  
  const handleOpenAddDialog = async () => {
    try {
      // Get TikTok auth URL
      const response = await axios.get('/api/auth/tiktok-auth-url', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      
      setAuthUrl(response.data.auth_url);
      setDialogType('add');
      setFormData({
        accountName: '',
        tiktokUsername: ''
      });
      setOpenDialog(true);
      
    } catch (error) {
      console.error('Error getting auth URL:', error);
      showSnackbar('Failed to get TikTok authorization URL', 'error');
    }
  };
  
  const handleOpenEditDialog = (account) => {
    setSelectedAccount(account);
    setFormData({
      accountName: account.account_name,
      tiktokUsername: account.tiktok_username
    });
    setDialogType('edit');
    setOpenDialog(true);
  };
  
  const handleCloseDialog = () => {
    setOpenDialog(false);
    setSelectedAccount(null);
  };
  
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };
  
  const handleAddAccount = async () => {
    // This would typically handle the OAuth flow with TikTok
    // For now, we'll simulate it
    
    window.open(authUrl, '_blank', 'width=800,height=600');
    
    // In a real implementation, you would have:
    // 1. User is redirected to TikTok authorization page
    // 2. After authorization, TikTok redirects back to your callback URL with an authorization code
    // 3. Your backend exchanges the code for an access token
    // 4. Backend creates a new account record
    
    showSnackbar('Please complete the TikTok authorization process in the new window', 'info');
    handleCloseDialog();
  };
  
  const handleEditAccount = async () => {
    try {
      await axios.put(`/api/accounts/${selectedAccount.id}`, {
        account_name: formData.accountName
      }, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      
      // Refresh accounts
      fetchAccounts();
      
      handleCloseDialog();
      showSnackbar('Account updated successfully', 'success');
      
    } catch (error) {
      console.error('Error updating account:', error);
      showSnackbar('Failed to update account', 'error');
    }
  };
  
  const handleDeleteAccount = async (accountId) => {
    const confirmDelete = window.confirm('Are you sure you want to delete this account? All scheduled posts for this account will also be deleted.');
    
    if (confirmDelete) {
      try {
        await axios.delete(`/api/accounts/${accountId}`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        
        // Refresh accounts
        fetchAccounts();
        
        showSnackbar('Account deleted successfully', 'success');
        
      } catch (error) {
        console.error('Error deleting account:', error);
        showSnackbar('Failed to delete account', 'error');
      }
    }
  };
  
  const handleRefreshToken = async (accountId) => {
    try {
      await axios.post(`/api/accounts/${accountId}/refresh-token`, {}, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      
      // Refresh accounts
      fetchAccounts();
      
      showSnackbar('Token refreshed successfully', 'success');
      
    } catch (error) {
      console.error('Error refreshing token:', error);
      showSnackbar('Failed to refresh token', 'error');
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
  
  // This function would be called when the user completes the TikTok OAuth flow
  // It would be triggered by a callback from the OAuth redirect
  const handleOAuthCallback = async (code) => {
    try {
      await axios.post('/api/accounts/complete-auth', {
        code,
        account_name: formData.accountName
      }, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      
      // Refresh accounts
      fetchAccounts();
      
      showSnackbar('Account added successfully', 'success');
      
    } catch (error) {
      console.error('Error completing auth:', error);
      showSnackbar('Failed to complete authorization', 'error');
    }
  };
  
  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1" sx={{ fontWeight: 'bold' }}>
          Manage TikTok Accounts
        </Typography>
        <Button 
          variant="contained" 
          color="primary" 
          startIcon={<AddIcon />}
          onClick={handleOpenAddDialog}
        >
          Add Account
        </Button>
      </Box>
      
      <Paper sx={{ p: 0 }}>
        {loading ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
            <CircularProgress sx={{ color: colors.brightRed }} />
          </Box>
        ) : accounts.length === 0 ? (
          <Box sx={{ p: 4, textAlign: 'center' }}>
            <Typography variant="body1" sx={{ mb: 2 }}>
              You don't have any TikTok accounts connected yet.
            </Typography>
            <Button 
              variant="contained" 
              color="primary" 
              startIcon={<AddIcon />}
              onClick={handleOpenAddDialog}
            >
              Add Your First Account
            </Button>
          </Box>
        ) : (
          <List sx={{ width: '100%' }}>
            {accounts.map((account, index) => (
              <React.Fragment key={account.id}>
                {index > 0 && <Divider component="li" />}
                <ListItem
                  secondaryAction={
                    <Box>
                      <IconButton 
                        edge="end" 
                        aria-label="refresh" 
                        onClick={() => handleRefreshToken(account.id)}
                        title="Refresh Token"
                      >
                        <RefreshIcon />
                      </IconButton>
                      <IconButton 
                        edge="end" 
                        aria-label="edit" 
                        sx={{ ml: 1 }}
                        onClick={() => handleOpenEditDialog(account)}
                      >
                        <EditIcon />
                      </IconButton>
                      <IconButton 
                        edge="end" 
                        aria-label="delete" 
                        sx={{ ml: 1 }}
                        onClick={() => handleDeleteAccount(account.id)}
                      >
                        <DeleteIcon />
                      </IconButton>
                    </Box>
                  }
                >
                  <ListItemAvatar>
                    <Avatar sx={{ bgcolor: colors.brightRed }}>
                      <PersonIcon />
                    </Avatar>
                  </ListItemAvatar>
                  <ListItemText
                    primary={
                      <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        <Typography variant="subtitle1" sx={{ fontWeight: 'bold' }}>
                          {account.account_name}
                        </Typography>
                        <Chip 
                          size="small" 
                          color={account.is_active ? "success" : "error"}
                          icon={account.is_active ? <CheckIcon /> : <CloseIcon />}
                          label={account.is_active ? "Active" : "Inactive"}
                          sx={{ ml: 2 }}
                        />
                      </Box>
                    }
                    secondary={
                      <>
                        <Typography component="span" variant="body2" color="text.primary">
                          @{account.tiktok_username}
                        </Typography>
                        {account.token_expiry && (
                          <Typography component="span" variant="body2" color="text.secondary" sx={{ ml: 2 }}>
                            Token expires: {new Date(account.token_expiry).toLocaleDateString()}
                          </Typography>
                        )}
                      </>
                    }
                  />
                </ListItem>
              </React.Fragment>
            ))}
          </List>
        )}
      </Paper>
      
      {/* Add/Edit Account Dialog */}
      <Dialog 
        open={openDialog} 
        onClose={handleCloseDialog}
        maxWidth="sm"
        fullWidth
        PaperProps={{
          sx: {
            borderRadius: '12px'
          }
        }}
      >
        <DialogTitle sx={{ backgroundColor: colors.black, color: 'white' }}>
          {dialogType === 'add' ? 'Add TikTok Account' : 'Edit Account'}
        </DialogTitle>
        
        <DialogContent sx={{ mt: 2 }}>
          <Box sx={{ my: 2 }}>
            <TextField
              label="Account Name"
              name="accountName"
              value={formData.accountName}
              onChange={handleInputChange}
              fullWidth
              margin="normal"
              placeholder="My TikTok Account"
              helperText="A friendly name to identify this account in the scheduler"
            />
            
            {dialogType === 'add' && (
              <Box sx={{ mt: 3 }}>
                <Typography variant="subtitle1" sx={{ fontWeight: 'bold', mb: 1 }}>
                  Connect with TikTok
                </Typography>
                <Typography variant="body2" sx={{ mb: 2 }}>
                  Click the button below to authorize this application to post to your TikTok account. You'll be redirected to TikTok's website to complete the authorization.
                </Typography>
                <Button 
                  variant="contained" 
                  color="primary" 
                  fullWidth
                  sx={{ mt: 1 }}
                  onClick={handleAddAccount}
                >
                  Connect to TikTok
                </Button>
              </Box>
            )}
          </Box>
        </DialogContent>
        
        <DialogActions sx={{ p: 2 }}>
          <Button onClick={handleCloseDialog} color="inherit">
            Cancel
          </Button>
          {dialogType === 'edit' && (
            <Button 
              onClick={handleEditAccount} 
              variant="contained" 
              color="primary"
              disabled={!formData.accountName}
            >
              Save Changes
            </Button>
          )}
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

export default AccountManager;