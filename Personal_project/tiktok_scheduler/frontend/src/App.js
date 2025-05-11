import React, { useState, useEffect } from 'react';
import { 
  ThemeProvider, 
  CssBaseline, 
  Box, 
  AppBar, 
  Toolbar, 
  Typography, 
  Drawer, 
  List, 
  ListItem, 
  ListItemIcon, 
  ListItemText, 
  IconButton, 
  Container, 
  Divider, 
  Avatar, 
  Menu, 
  MenuItem, 
  Button,
  CircularProgress
} from '@mui/material';
import { 
  Menu as MenuIcon, 
  Dashboard as DashboardIcon, 
  CalendarMonth as CalendarIcon, 
  Person as PersonIcon, 
  Settings as SettingsIcon, 
  Logout as LogoutIcon, 
  AccountCircle as AccountCircleIcon,
  AddCircle as AddCircleIcon,
  Help as HelpIcon
} from '@mui/icons-material';
import { styled } from '@mui/material/styles';
import theme, { colors } from './styles/theme';
import axios from 'axios';

// Import components
import Dashboard from './components/Dashboard';
import Calendar from './components/Calendar';
import PostForm from './components/PostForm';
import AccountManager from './components/AccountManager';
import Settings from './components/Settings';
import Login from './components/Login'; // Not shown in this file but would be needed

// Styled components
const drawerWidth = 240;

const Main = styled('main', { shouldForwardProp: (prop) => prop !== 'open' })(
  ({ theme, open }) => ({
    flexGrow: 1,
    transition: theme.transitions.create('margin', {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
    marginLeft: 0,
    ...(open && {
      transition: theme.transitions.create('margin', {
        easing: theme.transitions.easing.easeOut,
        duration: theme.transitions.duration.enteringScreen,
      }),
      marginLeft: drawerWidth,
    }),
  }),
);

const Logo = styled('div')(({ theme }) => ({
  display: 'flex',
  alignItems: 'center',
  padding: theme.spacing(0, 1),
  height: 64,
  backgroundColor: colors.black,
  color: 'white',
  fontWeight: 'bold',
  fontSize: '1.5rem',
  justifyContent: 'center',
}));

const StyledAppBar = styled(AppBar, { shouldForwardProp: (prop) => prop !== 'open' })(
  ({ theme, open }) => ({
    zIndex: theme.zIndex.drawer + 1,
    transition: theme.transitions.create(['width', 'margin'], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
    ...(open && {
      marginLeft: drawerWidth,
      width: `calc(100% - ${drawerWidth}px)`,
      transition: theme.transitions.create(['width', 'margin'], {
        easing: theme.transitions.easing.easeOut,
        duration: theme.transitions.duration.enteringScreen,
      }),
    }),
  }),
);

function App() {
  const [drawerOpen, setDrawerOpen] = useState(true);
  const [currentPage, setCurrentPage] = useState('dashboard');
  const [anchorEl, setAnchorEl] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);
  const [user, setUser] = useState(null);
  const [accounts, setAccounts] = useState([]);
  
  useEffect(() => {
    checkAuthentication();
  }, []);
  
  const checkAuthentication = async () => {
    const token = localStorage.getItem('token');
    
    if (!token) {
      setIsAuthenticated(false);
      setLoading(false);
      return;
    }
    
    try {
      // Verify token and get user info
      const response = await axios.get('/api/auth/user', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      setUser(response.data);
      setIsAuthenticated(true);
      
      // Fetch accounts
      fetchAccounts();
      
    } catch (error) {
      console.error('Authentication error:', error);
      localStorage.removeItem('token');
      setIsAuthenticated(false);
    } finally {
      setLoading(false);
    }
  };
  
  const fetchAccounts = async () => {
    try {
      const response = await axios.get('/api/dashboard/accounts', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      
      setAccounts(response.data.accounts);
    } catch (error) {
      console.error('Error fetching accounts:', error);
    }
  };
  
  const handleLogin = (token, userData) => {
    localStorage.setItem('token', token);
    setUser(userData);
    setIsAuthenticated(true);
    fetchAccounts();
  };
  
  const handleLogout = () => {
    localStorage.removeItem('token');
    setIsAuthenticated(false);
    setUser(null);
    setAccounts([]);
    setAnchorEl(null);
  };
  
  const handleDrawerToggle = () => {
    setDrawerOpen(!drawerOpen);
  };
  
  const handleMenuClick = (event) => {
    setAnchorEl(event.currentTarget);
  };
  
  const handleMenuClose = () => {
    setAnchorEl(null);
  };
  
  const handlePageChange = (page) => {
    setCurrentPage(page);
    setDrawerOpen(false);
  };
  
  if (loading) {
    return (
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
          <CircularProgress sx={{ color: colors.brightRed }} />
        </Box>
      </ThemeProvider>
    );
  }
  
  if (!isAuthenticated) {
    return (
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Login onLogin={handleLogin} />
      </ThemeProvider>
    );
  }
  
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ display: 'flex' }}>
        {/* App Bar */}
        <StyledAppBar position="fixed" open={drawerOpen}>
          <Toolbar>
            <IconButton
              color="inherit"
              aria-label="open drawer"
              onClick={handleDrawerToggle}
              edge="start"
              sx={{ mr: 2 }}
            >
              <MenuIcon />
            </IconButton>
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              TikTok Scheduler
            </Typography>
            
            <Button 
              color="inherit" 
              startIcon={<AddCircleIcon />}
              onClick={() => setCurrentPage('create')}
              sx={{ mr: 2 }}
            >
              New Post
            </Button>
            
            <IconButton
              color="inherit"
              onClick={handleMenuClick}
            >
              <Avatar sx={{ width: 32, height: 32, bgcolor: colors.brightRed }}>
                {user?.username?.charAt(0).toUpperCase() || 'U'}
              </Avatar>
            </IconButton>
            <Menu
              anchorEl={anchorEl}
              open={Boolean(anchorEl)}
              onClose={handleMenuClose}
              transformOrigin={{ horizontal: 'right', vertical: 'top' }}
              anchorOrigin={{ horizontal: 'right', vertical: 'bottom' }}
              PaperProps={{
                sx: {
                  mt: 1,
                  border: `1px solid ${colors.brightRed}`,
                  borderRadius: 2,
                }
              }}
            >
              <MenuItem onClick={() => { handleMenuClose(); setCurrentPage('profile'); }}>
                <ListItemIcon>
                  <AccountCircleIcon fontSize="small" />
                </ListItemIcon>
                <ListItemText>Profile</ListItemText>
              </MenuItem>
              <MenuItem onClick={() => { handleMenuClose(); setCurrentPage('settings'); }}>
                <ListItemIcon>
                  <SettingsIcon fontSize="small" />
                </ListItemIcon>
                <ListItemText>Settings</ListItemText>
              </MenuItem>
              <Divider />
              <MenuItem onClick={handleLogout}>
                <ListItemIcon>
                  <LogoutIcon fontSize="small" />
                </ListItemIcon>
                <ListItemText>Logout</ListItemText>
              </MenuItem>
            </Menu>
          </Toolbar>
        </StyledAppBar>
        
        {/* Drawer */}
        <Drawer
          variant="persistent"
          anchor="left"
          open={drawerOpen}
          sx={{
            width: drawerWidth,
            flexShrink: 0,
            '& .MuiDrawer-paper': {
              width: drawerWidth,
              boxSizing: 'border-box',
            },
          }}
        >
          <Logo>
            TikTok Scheduler
          </Logo>
          <List>
            <ListItem button selected={currentPage === 'dashboard'} onClick={() => setCurrentPage('dashboard')}>
              <ListItemIcon>
                <DashboardIcon />
              </ListItemIcon>
              <ListItemText primary="Dashboard" />
            </ListItem>
            <ListItem button selected={currentPage === 'calendar'} onClick={() => setCurrentPage('calendar')}>
              <ListItemIcon>
                <CalendarIcon />
              </ListItemIcon>
              <ListItemText primary="Calendar" />
            </ListItem>
            <ListItem button selected={currentPage === 'create'} onClick={() => setCurrentPage('create')}>
              <ListItemIcon>
                <AddCircleIcon />
              </ListItemIcon>
              <ListItemText primary="Create Post" />
            </ListItem>
            <ListItem button selected={currentPage === 'accounts'} onClick={() => setCurrentPage('accounts')}>
              <ListItemIcon>
                <PersonIcon />
              </ListItemIcon>
              <ListItemText primary="Accounts" />
            </ListItem>
            <Divider />
            <ListItem button selected={currentPage === 'settings'} onClick={() => setCurrentPage('settings')}>
              <ListItemIcon>
                <SettingsIcon />
              </ListItemIcon>
              <ListItemText primary="Settings" />
            </ListItem>
            <ListItem button onClick={() => window.open('https://developers.tiktok.com/doc/login-kit-web', '_blank')}>
              <ListItemIcon>
                <HelpIcon />
              </ListItemIcon>
              <ListItemText primary="TikTok API Docs" />
            </ListItem>
          </List>
        </Drawer>
        
        {/* Main Content */}
        <Main open={drawerOpen}>
          <Toolbar /> {/* Spacer */}
          <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
            {currentPage === 'dashboard' && <Dashboard />}
            {currentPage === 'calendar' && <Calendar accounts={accounts} />}
            {currentPage === 'create' && <PostForm accounts={accounts} onPostCreated={() => setCurrentPage('calendar')} />}
            {currentPage === 'accounts' && <AccountManager />}
            {currentPage === 'settings' && <Settings />}
          </Container>
        </Main>
      </Box>
    </ThemeProvider>
  );
}

export default App;