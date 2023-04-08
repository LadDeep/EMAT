import React, { useState } from 'react';
import { View } from 'react-native';
import GroupContext from './GroupContext';

const GroupProvider = ({ children }) => {
    const [groupState, setGroupState] = useState(false);

    return (
        <GroupContext.Provider value={{ groupState, setGroupState }}>
            {children}
        </GroupContext.Provider>
    );
};

export default GroupProvider;