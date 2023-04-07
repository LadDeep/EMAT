import React from 'react';
import { TouchableOpacity } from 'react-native';
import Icon from 'react-native-vector-icons/FontAwesome';

const GroupIcon = ({ onPress }) => (
    <TouchableOpacity onPress={onPress} style={{ position: 'absolute', bottom: 20, right: 20 }}>
        <Icon name="users" size={30} color="#000" />
    </TouchableOpacity>
);

export default GroupIcon;
