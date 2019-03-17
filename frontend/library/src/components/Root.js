import React from 'react';
import PropTypes from 'prop-types';

//material-ui
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';
import Paper from '@material-ui/core/Paper';
import SvgIcon from '@material-ui/core/SvgIcon';
import { withStyles } from '@material-ui/core/styles';

//inhouse
import FloorsNav from './floors_nav/FloorsNav.js';
import RoomTable from './room_table/RoomTable.js';
import RoomFilter from './room_filter/RoomFilter.js';
import Rooms from './rooms/Rooms.js';


//styles
const styles = theme => ({
    paper: {
        height: "100%",
        padding: 5
    },
    halfPaper: {
        height: "50%",
        padding: 5
    }
})

class Root extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            height: 0,
            floor: "",
            room: {},
            filter:{
                "occupied": true,
                "handicap accessible": false,
                "quiet": false
            }
        };
    }

    componentDidMount() {
        this.updateWindowDimensions();
        window.addEventListener("resize", this.updateWindowDimensions);
    }

    componentWillUnmount() {
        window.removeEventListener("resize", this.updateWindowDimensions);
    }

    updateWindowDimensions = () => {
        this.setState({
            height: window.innerHeight*.9,
            width: window.innerWidth*.99
        });
    }

    render() {
        const {classes, map} = this.props;
        let {floor, room, height, width, filter} = this.state;

        let {floors, rooms} = map;

        // handles when no floor is selected and there are no floor options
        if(floors.length > 0 && floor === "") {
            floor = floors[0];
        }

        //filter rooms down to floor
        rooms = rooms.filter((r)=>r.static_props.loc.floor === floor.name)

        return (
            <div styles={{flexGrow: 1}}>
            <AppBar
                position="static"
                color="primary">
                <Toolbar>
                    <Typography
                        variant="h4"
                        color="inherit">
                        Folsom Library
                    </Typography>
                </Toolbar>
            </AppBar>
            <Grid container spacing={8} style={{width: "100%"}}>
                <Grid item style={{height: height}} xs={2}>
                    <Paper className={classes.halfPaper}>
                        <FloorsNav
                            floor={floor}
                            floors={floors}
                            onClick={(f)=>this.setState({floor: f})}
                        />
                    </Paper>
                    <Paper className={classes.halfPaper}>
                        {JSON.stringify(room) !== "{}" &&
                            <RoomTable room={room} />
                        }
                        {JSON.stringify(room) === "{}" &&
                            <RoomFilter filter={filter} onFilterChange={(d)=>this.setState({filter: {...filter, ...d}})} />
                        }
                    </Paper>
                </Grid>
                <Grid item style={{height: height}} xs={10}>
                    <Paper className={classes.paper}>
                        <Rooms
                            filter={filter}
                            floor={floor}
                            rooms={rooms}
                            width={width*(10/12)}
                            height={height}
                            onRoomClick={(r)=>{this.setState({room: r})}}/>
                    </Paper>
                </Grid>
            </Grid>
            </div>
        );
    }
}

export default withStyles(styles)(Root);
