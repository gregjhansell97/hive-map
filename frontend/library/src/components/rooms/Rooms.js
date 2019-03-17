import React from 'react';
import PropTypes from 'prop-types';

//material-ui
import Button from '@material-ui/core/Button';
import { withStyles } from '@material-ui/core/styles';

//inhouse

//css
import './Rooms.css'

//styles
const styles = theme => ({
    button: {
        textTransform: "none",
        width: "100%",
        fontSize: "30px",
        marginTop: 3
    }
})

//reactcode

class Rooms extends React.Component {
    constructor(props) {
        super(props);
        this.canvasRef = React.createRef();
    }

    onCanvasClick = (canvas, x, y) => {
        const {floor, rooms, width, height, onRoomClick} = this.props;
        if(floor === "") return;

        x = (x*floor.dim.x)/canvas.width;
        y = (y*floor.dim.y)/canvas.height;

        for(let r of rooms) {
            if(x < r.static_props.loc.x) continue;
            if(x > r.static_props.loc.x + r.static_props.dim.x) continue;
            if(y < r.static_props.loc.y) continue;
            if(y > r.static_props.loc.y + r.static_props.dim.y) continue;
            onRoomClick(r);
            return;
        }
        onRoomClick({});;

    }

    renderCanvas() {
        const {floor, filter, rooms, width, height} = this.props;
        if(floor === "") return;
        const canvas = this.canvasRef.current;

        canvas.width = width;
        canvas.height = height;
        canvas.onclick = (event)=>this.onCanvasClick(canvas, event.offsetX, event.offsetY);
        const context = canvas.getContext('2d');

        const width_ratio = canvas.width/floor.dim.x;
        const height_ratio = canvas.height/floor.dim.y;

        context.clearRect(0, 0, canvas.width, canvas.height);
        for(let r of rooms) {
            //adjust location to fit canvas
            const rect_x = parseInt(r.static_props.loc.x*width_ratio - 0.65);
            const rect_y = parseInt(r.static_props.loc.y*height_ratio - 0.65);

            //adjust size to fit canvas
            const rect_width = parseInt(r.static_props.dim.x*width_ratio - 0.65);
            const rect_height = parseInt(r.static_props.dim.y*height_ratio - 0.65);



            //decide on color
            context.fillStyle = "#388E3C"; //greeen
            let makeRed = filter["occupied"] && r.dynamic_props.occupied;
            makeRed = makeRed || filter["handicap accessible"] && "handicap accessible" in r.static_props && !r.static_props["handicap accessible"]
            makeRed = makeRed || filter["quiet"] && "quiet" in r.dynamic_props && !r.dynamic_props["quiet"]
            if(makeRed) {
                context.fillStyle = "#E53935";
            }

            context.fillRect(rect_x, rect_y, rect_width, rect_height)
            context.font="35px Arial";
            context.textAlign="center";
            context.textBaseline = "middle";
            context.fillStyle = "#FFFFFF";
            context.fillText(r.name,rect_x + (rect_width/2), rect_y+(rect_height/2));
        }
    }

    render() {
        const {classes, rooms, floor} = this.props;
        this.renderCanvas();
        return (
            <div>
                <canvas ref={this.canvasRef} className="canvas"/>
            </div>
        );
    }
}

export default withStyles(styles)(Rooms);
