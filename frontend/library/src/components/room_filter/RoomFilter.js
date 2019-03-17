import React from 'react';
import PropTypes from 'prop-types';


//material-ui
import FormGroup from '@material-ui/core/FormGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Switch from '@material-ui/core/Switch';
import Input from '@material-ui/core/Input'
import { withStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Button from '@material-ui/core/Button';
import NativeSelect from '@material-ui/core/NativeSelect';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';

//inhouse

//styles
const styles = theme => ({
    formControl: {
      margin: theme.spacing.unit,
      justifyContent: "center"
    },
})

//reactcode

class RoomFilter extends React.Component {

    render() {
        const {classes, filter, onFilterChange} = this.props;
        return (
            <div>
            <AppBar
                position="static"
                color="primary">
                <Toolbar>
                    <Typography
                        variant="h4"
                        color="inherit">
                        Filters
                    </Typography>
                </Toolbar>
            </AppBar>
            <FormGroup className={classes.formControl}>
                {Object.entries(filter).map(([k, v], index) =>
                    <FormControlLabel
                        key={index}
                        control={
                            <div>
                                {(typeof v) === "number" && <NativeSelect
                                    value={v}
                                    onChange={(e) => onFilterChange({[k]: e.target.value})}
                                    name={k} >
                                        <option value={1}>1</option>
                                        <option value={2}>2</option>
                                        <option value={3}>3</option>
                                        <option value={4}>4</option>
                                        <option value={5}>5</option>
                                        <option value={6}>6</option>
                                </NativeSelect>}
                                {(typeof v) === "boolean" && <Switch
                                    checked={v}
                                    onChange={(e) => onFilterChange({[k]: !v})} />
                                }
                            </div>
                        }
                        label={
                            <Typography
                                variant="h6"
                                color="default">
                                {k}
                            </Typography>
                        }
                    />
                )}
            </FormGroup>
            </div>
        );
    }
}

/*
<Switch
    checked={v}
    onChange={(e) => console.log(!v)} />
*/

export default withStyles(styles)(RoomFilter);
