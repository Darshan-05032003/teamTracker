import { useState } from 'react'
import './App.css'
import {
  AppBar,
  Box,
  CssBaseline,
  Drawer,
  IconButton,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Toolbar,
  Typography,
  Card,
  CardContent,
  Grid,
  TextField,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Avatar,
  Chip,
  useTheme,
  useMediaQuery,
} from '@mui/material'
import MenuIcon from '@mui/icons-material/Menu'
import DashboardIcon from '@mui/icons-material/Dashboard'
import PeopleIcon from '@mui/icons-material/People'
import BusinessIcon from '@mui/icons-material/Business'
import WorkIcon from '@mui/icons-material/Work'
import SearchIcon from '@mui/icons-material/Search'
import PersonIcon from '@mui/icons-material/Person'

// Sample employee data
const sampleEmployees = [
  {
    id: 1,
    name: 'John Doe',
    department: 'Engineering',
    position: 'Software Engineer',
    email: 'john.doe@company.com',
    joinDate: '2023-01-15',
    status: 'Active',
  },
  {
    id: 2,
    name: 'Jane Smith',
    department: 'Marketing',
    position: 'Marketing Manager',
    email: 'jane.smith@company.com',
    joinDate: '2023-02-20',
    status: 'Active',
  },
  {
    id: 3,
    name: 'Robert Johnson',
    department: 'Engineering',
    position: 'DevOps Engineer',
    email: 'robert.johnson@company.com',
    joinDate: '2023-03-10',
    status: 'On Leave',
  },
  {
    id: 4,
    name: 'Emily Davis',
    department: 'Human Resources',
    position: 'HR Specialist',
    email: 'emily.davis@company.com',
    joinDate: '2023-04-05',
    status: 'Active',
  },
  {
    id: 5,
    name: 'Michael Brown',
    department: 'Sales',
    position: 'Sales Representative',
    email: 'michael.brown@company.com',
    joinDate: '2023-05-12',
    status: 'Active',
  },
  {
    id: 6,
    name: 'Sarah Wilson',
    department: 'Engineering',
    position: 'Frontend Developer',
    email: 'sarah.wilson@company.com',
    joinDate: '2023-06-18',
    status: 'Inactive',
  },
  {
    id: 7,
    name: 'David Lee',
    department: 'Marketing',
    position: 'Content Writer',
    email: 'david.lee@company.com',
    joinDate: '2023-07-22',
    status: 'Active',
  },
  {
    id: 8,
    name: 'Lisa Anderson',
    department: 'Engineering',
    position: 'Backend Developer',
    email: 'lisa.anderson@company.com',
    joinDate: '2023-08-30',
    status: 'Active',
  },
]

function App() {
  const [searchTerm, setSearchTerm] = useState('')
  const [isDrawerOpen, setIsDrawerOpen] = useState(false)
  const theme = useTheme()
  const isMobile = useMediaQuery(theme.breakpoints.down('md'))

  const filteredEmployees = sampleEmployees.filter((employee) => {
    const matchesName = employee.name.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesDepartment = employee.department.toLowerCase().includes(searchTerm.toLowerCase())
    return matchesName || matchesDepartment
  })

  const handleSearchChange = (event) => {
    setSearchTerm(event.target.value)
  }

  const toggleDrawer = () => {
    setIsDrawerOpen(!isDrawerOpen)
  }

  const drawerWidth = 240

  const getStatusColor = (status) => {
    switch (status) {
      case 'Active':
        return 'success'
      case 'On Leave':
        return 'warning'
      case 'Inactive':
        return 'error'
      default:
        return 'default'
    }
  }

  return (
    <Box sx={{ display: 'flex' }}>
      <CssBaseline />
      <AppBar
        position="fixed"
        sx={{ zIndex: theme.zIndex.drawer + 1, bgcolor: '#1976d2' }}
      >
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            onClick={toggleDrawer}
            edge="start"
            sx={{ mr: 2, display: { md: 'none' } }}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" noWrap component="div" sx={{ flexGrow: 1 }}>
            TeamTrack
          </Typography>
        </Toolbar>
      </AppBar>

      <Drawer
        variant={isMobile ? 'temporary' : 'permanent'}
        open={isDrawerOpen}
        onClose={toggleDrawer}
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          '& .MuiDrawer-paper': {
            width: drawerWidth,
            boxSizing: 'border-box',
          },
        }}
      >
        <Toolbar />
        <Box sx={{ overflow: 'auto' }}>
          <List>
            <ListItem button>
              <ListItemIcon>
                <DashboardIcon />
              </ListItemIcon>
              <ListItemText primary="Dashboard" />
            </ListItem>
            <ListItem button>
              <ListItemIcon>
                <PeopleIcon />
              </ListItemIcon>
              <ListItemText primary="Employees" />
            </ListItem>
          </List>
        </Box>
      </Drawer>

      <Box component="main" sx={{ flexGrow: 1, p: 3, width: { md: `calc(100% - ${drawerWidth}px)` }, ml: { md: `${drawerWidth}px` } }}>
        <Toolbar />

        {/* Summary Cards */}
        <Grid container spacing={3} sx={{ mb: 4 }}>
          <Grid item xs={12} sm={6} md={4}>
            <Card sx={{ height: '100%', bgcolor: '#e3f2fd' }}>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  <Avatar sx={{ bgcolor: '#1976d2', mr: 2 }}>
                    <PeopleIcon />
                  </Avatar>
                  <Box>
                    <Typography variant="h5" component="div">
                      {sampleEmployees.length}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Total Employees
                    </Typography>
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} sm={6} md={4}>
            <Card sx={{ height: '100%', bgcolor: '#f3e5f5' }}>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  <Avatar sx={{ bgcolor: '#7b1fa2', mr: 2 }}>
                    <BusinessIcon />
                  </Avatar>
                  <Box>
                    <Typography variant="h5" component="div">
                      {
                        new Set(sampleEmployees.map((emp) => emp.department)).size
                      }
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Departments
                    </Typography>
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} sm={6} md={4}>
            <Card sx={{ height: '100%', bgcolor: '#e8f5e8' }}>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  <Avatar sx={{ bgcolor: '#2e7d32', mr: 2 }}>
                    <WorkIcon />
                  </Avatar>
                  <Box>
                    <Typography variant="h5" component="div">
                      {
                        sampleEmployees.filter((emp) => emp.status === 'Active').length
                      }
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Active Employees
                    </Typography>
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        </Grid>

        {/* Employee Directory */}
        <Paper sx={{ p: 3 }} elevation={3}>
          <Box sx={{ mb: 3, display: 'flex', alignItems: 'center', gap: 2 }}>
            <SearchIcon color="action" />
            <Typography variant="h6">Employee Directory</Typography>
          </Box>

          <TextField
            fullWidth
            variant="outlined"
            placeholder="Search by name or department..."
            value={searchTerm}
            onChange={handleSearchChange}
            sx={{ mb: 3 }}
          />

          {filteredEmployees.length === 0 ? (
            <Box sx={{ textAlign: 'center', py: 4 }}>
              <Typography variant="body1" color="text.secondary">
                No employees found matching your search.
              </Typography>
            </Box>
          ) : (
            <TableContainer component={Paper} variant="outlined">
              <Table>
                <TableHead>
                  <TableRow sx={{ bgcolor: '#f5f5f5' }}>
                    <TableCell>Employee</TableCell>
                    <TableCell>Department</TableCell>
                    <TableCell>Position</TableCell>
                    <TableCell>Status</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {filteredEmployees.map((employee) => (
                    <TableRow key={employee.id} hover>
                      <TableCell>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                          <Avatar sx={{ bgcolor: '#1976d2' }} size="small">
                            <PersonIcon fontSize="small" />
                          </Avatar>
                          <Box>
                            <Typography variant="body1" fontWeight="medium">
                              {employee.name}
                            </Typography>
                            <Typography variant="body2" color="text.secondary">
                              {employee.email}
                            </Typography>
                          </Box>
                        </Box>
                      </TableCell>
                      <TableCell>
                        <Chip
                          label={employee.department}
                          size="small"
                          sx={{ bgcolor: '#e3f2fd', color: '#1976d2' }}
                        />
                      </TableCell>
                      <TableCell>{employee.position}</TableCell>
                      <TableCell>
                        <Chip
                          label={employee.status}
                          size="small"
                          color={getStatusColor(employee.status)}
                          variant="filled"
                        />
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          )}
        </Paper>
      </Box>
    </Box>
  )
}

export default App
