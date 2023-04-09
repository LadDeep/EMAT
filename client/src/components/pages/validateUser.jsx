import React, { useState } from 'react';
import { View, Text, TextInput, Button, Alert, StyleSheet } from 'react-native';
import { useNavigation } from "@react-navigation/native";
import { ValidateUserRegistration } from '../../api/api';
function valdateUser({ route }) {
    const [token, setToken] = useState('');
    const { response } = route.params;
    const navigation = useNavigation();

    console.log("This is response//////////////", response)
    const handleValidation = () => {
        ValidateUserRegistration(response, token,
            (res) => {
                console.log("This is response of updated Expenses", res.data.response)
            },
            (err) => { console.log("err", err) })

        // if (!code) {
        //     Alert.alert("", 'Enter Some Value');
        //     return;
        // }
        // handleSubmit();
    };

    const handleSubmit = () => {
        ValidateUserRegistration(response, token,
            (res) => {
                console.log("This is response of updated Expenses", res.data.response.verified)
                if (res.data.response.verified) {

                    navigation.navigate("SignIn")
                } else {
                    alert("Enter a valid Token")
                }
            },
            (err) => { console.log("err", err) })

        // Code to send 
        // console.log(code)
        // JoinGroupApi(code, (response) => {
        //     if (response.data.status) {
        //         Alert.alert("", 'Group Joined');
        //         navigation.push("GroupsTab")
        //     }
        // }, (err) => {
        //     console.log(err)
        // })

    };

    return (
        <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
            <Text style={styles.passwordRecoveryText}>Enter Validation Token</Text>
            <TextInput
                style={{ height: 40, borderColor: 'gray', borderWidth: 1, width: '80%', margin: 10, padding: 5 }}
                placeholder="Enter your token"
                onChangeText={(text) => setToken(text)}
                value={token}
                keyboardType="text"
            />
            <Button
                title="Submit"
                onPress={handleSubmit}
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

export default valdateUser;