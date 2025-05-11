import React, { useState, useEffect } from 'react';
import { 
  Box, 
  Paper, 
  Typography, 
  Grid, 
  Card, 
  CardContent, 
  Table, 
  TableBody, 
  TableCell, 
  TableContainer, 
  TableHead, 
  TableRow,
  IconButton,
  Button,
  Chip,
  CircularProgress
} from '@mui/material';
import { 
  Schedule as ScheduleIcon,
  CheckCircle as CheckCircleIcon,
  Error as ErrorIcon,
  AccountCircle as AccountCircleIcon,
  Edit as EditIcon,
  Delete as DeleteIcon
} from '@mui/icons-material';
import { colors } from '../styles/theme';
import axios from 'axios';
import { format } from 'date-fns';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const StatCard = ({ title, value, icon, color }) => (
  <Card sx={{ height: '100%' }}>
    <CardContent>
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
        <Box sx={{ 
          display: 'flex', 
          alignItems: 'center', 
          justifyContent: 'center', 
          backgroundColor: `${color}20`, 
          color: color, 
          width: 48, 
          height: 48, 
          borderRadius: '50%', 
          mr: 2 
        }}>
          {icon}
        </Box>
        <Typography variant="h6" color="text.secondary">
          {title}
        </Typography>
      </Box>
      <Typography variant="h3" sx={{ fontWeight: 'bold' }}>
        {value}
      </Typography>
    </CardContent>
  </Card>
);

const Dashboard = () => {
  const [stats, setStats] = useState(null);
  const [monthlyStats, setMonthlyStats] = useState([]);
  const [failedPosts, setFailedPosts] = useState([]);
  const [upcomingPosts, setUpcomingPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    fetchDashboardData();
  }, []);
  
  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      
      // Fetch all data in parallel
      const [statsRes, monthlyStatsRes, failedPostsRes, upcomingPostsRes] = await Promise.all([
        axios.get('/api/dashboard/stats', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        }),
        axios.get('/api/dashboard/monthly-stats', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        }),
        axios.get('/api/dashboard/failed-posts', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        }),
        axios.get('/api/dashboard/upcoming-posts', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        })
      ]);
      
      setStats(statsRes.data);
      setMonthlyStats(monthlyStatsRes.data.monthly_stats);
      setFailedPosts(failedPostsRes.data.failed_posts);
      setUpcomingPosts(upcomingPostsRes.data.upcoming_posts);
      setLoading(false);
      
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
      setLoading(false);
    }
  };
  
  const handleRetryPost = async (postId) => {
    try {
      // Implementation would depend on how retrying is handled in the backend
      alert('Retry functionality would be implemented here');
      // Refresh data after retry
      fetchDashboardData();
    } catch (error) {
      console.error('Error retrying post:', error);
    }
  };
  
  const handleDeletePost = async (postId) => {
    try {
      await axios.delete(`/api/scheduler/cancel/${postId}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      
      // Refresh data after deletion
      fetchDashboardData();
      
    } catch (error) {
      console.error('Error deleting post:', error);
    }
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
        Dashboard
      </Typography>
      
      {/* Stats Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard 
            title="Total Posts" 
            value={stats?.total_posts || 0} 
            icon={<ScheduleIcon fontSize="large" />} 
            color={colors.brightRed} 
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard 
            title="Scheduled" 
            value={stats?.scheduled_posts || 0} 
            icon={<ScheduleIcon fontSize="large" />} 
            color="#1976d2" 
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard 
            title="Published" 
            value={stats?.sent_posts || 0} 
            icon={<CheckCircleIcon fontSize="large" />} 
            color="#4caf50" 
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard 
            title="Failed" 
            value={stats?.failed_posts || 0} 
            icon={<ErrorIcon fontSize="large" />} 
            color="#f44336" 
          />
        </Grid>
      </Grid>
      
      {/* Monthly Stats Chart */}
      <Paper sx={{ p: 3, mb: 4 }}>
        <Typography variant="h6" sx={{ mb: 2 }}>
          Monthly Statistics
        </Typography>
        <Box sx={{ height: 300 }}>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={monthlyStats}
              margin={{
                top: 20,
                right: 30,
                left: 20,
                bottom: 5,
              }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="scheduled" fill="#1976d2" name="Scheduled" />
              <Bar dataKey="sent" fill="#4caf50" name="Published" />
              <Bar dataKey="failed" fill="#f44336" name="Failed" />
            </BarChart>
          </ResponsiveContainer>
        </Box>
      </Paper>
      
      {/* Upcoming Posts Table */}
      <Paper sx={{ p: 3, mb: 4 }}>
        <Typography variant="h6" sx={{ mb: 2 }}>
          Upcoming Posts
        </Typography>
        
        {upcomingPosts.length === 0 ? (
          <Typography variant="body1" sx={{ textAlign: 'center', p: 2 }}>
            No upcoming posts scheduled. Go to the calendar to schedule new posts.
          </Typography>
        ) : (
          <TableContainer>
            <Table sx={{ minWidth: 650 }}>
              <TableHead>
                <TableRow>
                  <TableCell>Caption</TableCell>
                  <TableCell>Scheduled For</TableCell>
                  <TableCell>Account</TableCell>
                  <TableCell>Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {upcomingPosts.slice(0, 5).map((post) => (
                  <TableRow key={post.id}>
                    <TableCell sx={{ maxWidth: 200, overflow: 'hidden', textOverflow: 'ellipsis' }}>
                      {post.caption || '(No caption)'}
                    </TableCell>
                    <TableCell>
                      {format(new Date(post.scheduled_time), 'MMM d, yyyy h:mm a')}
                    </TableCell>
                    <TableCell>Account #{post.account_id}</TableCell>
                    <TableCell>
                      <IconButton size="small" color="primary">
                        <EditIcon />
                      </IconButton>
                      <IconButton 
                        size="small" 
                        color="error" 
                        onClick={() => handleDeletePost(post.id)}
                      >
                        <DeleteIcon />
                      </IconButton>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        )}
        
        {upcomingPosts.length > 5 && (
          <Box sx={{ textAlign: 'center', mt: 2 }}>
            <Button variant="text" color="primary">
              View All ({upcomingPosts.length})
            </Button>
          </Box>
        )}
      </Paper>
      
      {/* Failed Posts Table */}
      <Paper sx={{ p: 3 }}>
        <Typography variant="h6" sx={{ mb: 2 }}>
          Failed Posts
        </Typography>
        
        {failedPosts.length === 0 ? (
          <Typography variant="body1" sx={{ textAlign: 'center', p: 2 }}>
            No failed posts. Everything is running smoothly!
          </Typography>
        ) : (
          <TableContainer>
            <Table sx={{ minWidth: 650 }}>
              <TableHead>
                <TableRow>
                  <TableCell>Caption</TableCell>
                  <TableCell>Scheduled For</TableCell>
                  <TableCell>Error</TableCell>
                  <TableCell>Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {failedPosts.slice(0, 5).map((post) => (
                  <TableRow key={post.id}>
                    <TableCell sx={{ maxWidth: 200, overflow: 'hidden', textOverflow: 'ellipsis' }}>
                      {post.caption || '(No caption)'}
                    </TableCell>
                    <TableCell>
                      {format(new Date(post.scheduled_time), 'MMM d, yyyy h:mm a')}
                    </TableCell>
                    <TableCell sx={{ maxWidth: 300, overflow: 'hidden', textOverflow: 'ellipsis' }}>
                      {post.error_message || 'Unknown error'}
                    </TableCell>
                    <TableCell>
                      <Button 
                        variant="contained" 
                        color="primary" 
                        size="small"
                        onClick={() => handleRetryPost(post.id)}
                      >
                        Retry
                      </Button>
                      <IconButton 
                        size="small" 
                        color="error" 
                        sx={{ ml: 1 }}
                        onClick={() => handleDeletePost(post.id)}
                      >
                        <DeleteIcon />
                      </IconButton>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        )}
        
        {failedPosts.length > 5 && (
          <Box sx={{ textAlign: 'center', mt: 2 }}>
            <Button variant="text" color="primary">
              View All ({failedPosts.length})
            </Button>
          </Box>
        )}
      </Paper>
    </Box>
  );
};

export default Dashboard;