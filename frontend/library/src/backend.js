import axios from 'axios';
import store from './flux/store.js';
import {
    setMap
} from './flux/actions.js';
import data from "./data.json"

export default {
    refreshMap: function() {
        /**
         * grabs the most up-to-date map
         */
        const hosts = ["127.0.0.1:8080"]
        const host = hosts[Math.floor(Math.random()*hosts.length)];
        axios.get("http://" + host + "/full_update") //it /hivemap/rpi/get_map
        .then(response => {
            console.log(response.data);
            store.dispatch(setMap(response.data));
        })
        .catch(error => {
            console.log("HERE :(")
            store.dispatch(setMap(data));
            /*store.dispatch(setMap({
                floors: [
                    {
                        name: "First Floor",
                        dim: {
                            x: 100,
                            y: 100
                        }
                    },
                    {
                        name: "Second Floor",
                        dim: {
                            x: 100,
                            y: 100
                        }
                    },
                    {
                        name: "Third Floor",
                        dim: {
                            x: 100,
                            y: 100
                        }
                    },
                ],
                rooms: [
                    {
                        name: "room_1",
                        static_props: {
                            loc: {
                                x: 0,
                                y: 0,
                                floor: "First Floor"
                            },
                            dim: {
                                x: 30,
                                y: 50
                            }
                        },
                        dynamic_props: {
                            occupied: true
                        }
                    },
                    {
                        name: "room_2",
                        static_props: {
                            loc: {
                                x: 0,
                                y: 50,
                                floor: "First Floor"
                            },
                            dim: {
                                x: 50,
                                y: 30
                            }
                        },
                        dynamic_props: {
                            occupied: true
                        }
                    }
                ]
            })); */
        })

    }
}
