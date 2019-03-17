export const MAP = "MAP";

/**
 * starting out with just one action of setting the map, could add new store
 * items if map needs to be differentiated between buildings/areas (likely not)
 */
export const setMap = map => ({
    type: MAP,
    execute: function(state={}){
        return map;
    }
});
