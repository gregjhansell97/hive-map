import React from 'react';
import ReactDOM from 'react-dom';
import {
    connect,
    Provider
} from 'react-redux';

//inhouse
import * as serviceWorker from './serviceWorker.js';
import backend from './backend.js'
import Root from './components/Root.js';
import store from './flux/store.js';

//css
import './index.css';

function mapStateToProps(state, props) {
    return {
        map: state.map
    }
}

const ConnectedRoot = connect(mapStateToProps)(Root);

ReactDOM.render(
    <Provider store={store}>
        <ConnectedRoot />
    </Provider>, document.getElementById('root'));

setInterval(()=>backend.refreshMap(), 1000);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
