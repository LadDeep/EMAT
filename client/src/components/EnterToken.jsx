import React, { useState } from 'react';
import { View, Text, TextInput, Button, Alert, StyleSheet } from 'react-native';
import { ForgotPassword } from '../api/api';
import { useNavigation } from '@react-navigation/native';
import { useEffect } from 'react';

function EnterToken({ route }) {
    const [usertoken, setUserToken] = useState('');
    const navigation = useNavigation();
    let { token } = route.params;
    useEffect(() => {
        token = token !== undefined ? token : ""
        setUserToken(token)
    }, [])



    const handleValidation = () => {
        if (token.length === 0) {
            Alert.alert("Empty Token", 'Enter token from the email sent to you.');
            return;
        }
        handleSubmit();
    };

    const handleSubmit = () => {
        navigation.navigate("PasswordReset", { token: usertoken })

    };

    return (
        <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
            <Text style={styles.passwordRecoveryText}>Enter Token</Text>
            <TextInput
                style={{ height: 40, borderColor: 'gray', borderWidth: 1, width: '80%', margin: 10, padding: 5 }}
                placeholder="Enter your token"
                onChangeText={text => setUserToken(text)}
                value={usertoken}
                keyboardType="text"
            />
            <Button
                title="Submit"
                onPress={handleValidation}
            />
        </View>
    );

}
const styles = StyleSheet.create({
    passwordRecoveryText: {
        fontSize: 24,
        fontWeight: 'bold',
        marginBottom: 20,
    },
});

export default EnterToken;