import React from 'react';
import PropTypes from 'prop-types';


//material-ui
import Button from '@material-ui/core/Button';
import { withStyles } from '@material-ui/core/styles';

//inhouse

//styles
const styles = theme => ({
    button: {
        textTransform: "none",
        width: "100%",
        fontSize: "30px",
        marginTop:3
    }
})

//reactcode

class FloorsNav extends React.Component {
    render() {
        const {classes, floor, floors, onClick} = this.props;
        return (
            <div>
                {floors.map((f, index) => (
                    <Button
                        disableRipple
                        key={index}
                        variant={(f.name === floor.name ? "contained" : "outlined")}
                        color="primary"
                        className={classes.button}
                        onClick={(e)=>onClick(f)}>
                        {f.name}
                    </Button>
                ))}
            </div>
        );
    }
}

export default withStyles(styles)(FloorsNav);
