import React from 'react';
import PropTypes from 'prop-types';

//material-ui
import AppBar from '@material-ui/core/AppBar';
import Button from '@material-ui/core/Button';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import { withStyles } from '@material-ui/core/styles';

//inhouse

//styles
const styles = theme => ({
  root: {
    width: '100%',
    marginTop: theme.spacing.unit * 3,
    overflowX: 'auto',
  },
  table: {
    width: "90%",
  },
});

//reactcode

class RoomTable extends React.Component {
    render() {
        const {classes, room} = this.props;
        if(room.dynamic_props === undefined || room.static_props === undefined) {
            return (<h1>hello world</h1>)
        }

        let room_fields = {};
        for(let d_field of Object.keys(room.dynamic_props)){
            const d_value = room.dynamic_props[d_field];
            if(["boolean", "number"].includes(typeof d_value)){
                room_fields[d_field] = JSON.stringify(d_value);
            }else if(typeof d_value === "string") {
                room_fields[d_field] = d_value;
            }
        }
        for(let d_field of Object.keys(room.static_props)){
            const d_value = room.static_props[d_field];
            if(["boolean", "number"].includes(typeof d_value)){
                room_fields[d_field] = JSON.stringify(d_value);
            }else if(typeof d_value === "string") {
                room_fields[d_field] = d_value;
            }
        }


        return (
            <div>
            <AppBar
                position="static"
                color="primary">
            <Toolbar>
                <Typography
                    variant="h4"
                    color="inherit">
                    Status
                </Typography>
            </Toolbar>
                        </AppBar>
            <Table className={classes.table}>
            <TableBody>
                {Object.entries(room_fields).map(([f, v], index) => (
                    <TableRow key={index}>
                        <TableCell>
                            <Typography
                                variant="h6"
                                color="primary">
                                {f}
                            </Typography>
                        </TableCell>
                        <TableCell>
                            <Typography
                                variant="h6"
                                color="default">
                                {v}
                            </Typography>
                        </TableCell>
                    </TableRow>
                ))}
              </TableBody>
            </Table>
            </div>
        );
    }
}

/*

*/

export default withStyles(styles)(RoomTable);
