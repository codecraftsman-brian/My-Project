import { createTheme } from '@mui/material/styles';

// Color palette from requirements
const colors = {
  black: '#000000',
  darkRed: '#3D0000',
  mediumRed: '#950101',
  brightRed: '#FF0000'
};

const theme = createTheme({
  palette: {
    primary: {
      main: colors.brightRed,
      dark: colors.mediumRed,
      darker: colors.darkRed,
      contrastText: '#fff',
    },
    secondary: {
      main: colors.darkRed,
      light: colors.mediumRed,
      contrastText: '#fff',
    },
    background: {
      default: '#f5f5f5',
      paper: '#fff',
      dark: colors.black,
    },
    text: {
      primary: colors.black,
      secondary: '#666',
      disabled: '#999',
    },
    error: {
      main: colors.brightRed,
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    h1: {
      fontWeight: 700,
      fontSize: '2.5rem',
    },
    h2: {
      fontWeight: 600,
      fontSize: '2rem',
    },
    h3: {
      fontWeight: 600,
      fontSize: '1.75rem',
    },
    h4: {
      fontWeight: 600,
      fontSize: '1.5rem',
    },
    h5: {
      fontWeight: 500,
      fontSize: '1.25rem',
    },
    h6: {
      fontWeight: 500,
      fontSize: '1rem',
    },
    button: {
      fontWeight: 500,
      textTransform: 'none',
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          padding: '8px 16px',
          fontWeight: 500,
        },
        containedPrimary: {
          backgroundColor: colors.brightRed,
          '&:hover': {
            backgroundColor: colors.mediumRed,
          },
        },
        outlinedPrimary: {
          borderColor: colors.brightRed,
          color: colors.brightRed,
          '&:hover': {
            borderColor: colors.mediumRed,
            backgroundColor: 'rgba(255, 0, 0, 0.04)',
          },
        },
      },
    },
    MuiTextField: {
      styleOverrides: {
        root: {
          '& .MuiOutlinedInput-root': {
            '&.Mui-focused fieldset': {
              borderColor: colors.brightRed,
            },
          },
          '& .MuiInputLabel-root.Mui-focused': {
            color: colors.brightRed,
          },
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          borderRadius: 12,
          boxShadow: '0px 3px 15px rgba(0, 0, 0, 0.05)',
        },
      },
    },
    MuiAppBar: {
      styleOverrides: {
        root: {
          backgroundColor: colors.black,
          color: '#fff',
        },
      },
    },
    MuiTab: {
      styleOverrides: {
        root: {
          '&.Mui-selected': {
            color: colors.brightRed,
          },
        },
      },
    },
    MuiTabs: {
      styleOverrides: {
        indicator: {
          backgroundColor: colors.brightRed,
        },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: {
          '&.MuiChip-colorPrimary': {
            backgroundColor: colors.brightRed,
          },
          '&.MuiChip-colorSecondary': {
            backgroundColor: colors.darkRed,
          },
        },
      },
    },
  },
});

export default theme;
export { colors };