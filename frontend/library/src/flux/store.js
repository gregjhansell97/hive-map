import { combineReducers, createStore } from 'redux';

import {
    MAP
} from './actions.js';

const map = (state = {floors: [], rooms:[]}, action) => {
    if(action.type === MAP) {
        return action.execute(state);
    } else {
        return state;
    }
}

const reducers = combineReducers({
    map
});

export default createStore(reducers);
