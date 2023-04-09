import React, { useState } from 'react';
import { View, Text, TextInput, Button, Alert, StyleSheet } from 'react-native';
import { ForgotPassword } from '../api/api';
import { useNavigation } from '@react-navigation/native';

function PasswordRecovery() {
  const [email, setEmail] = useState('');
  const navigation = useNavigation();

  const handleValidation = () => {
    const emailRegex = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
    if (!emailRegex.test(email)) {
      Alert.alert('Invalid email', 'Please enter a valid email address.');
      return;
    }
    handleSubmit();
  };

  const handleSubmit = () => {
    // Code to send password recovery email
    Alert.alert("", 'Email sent Successfully');
    let payload = { email: email }
    console.log("PAYLOAD", payload)
    ForgotPassword(payload,
      (res) => {
        console.log("Response of Forgot Password", res.data.reset_token)
        navigation.navigate("EnterToken", { token: res.data.reset_token })
      }
      ,
      (err) => { console.log(err) })
  };

  return (
    <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
      <Text style={styles.passwordRecoveryText}>Password Recovery</Text>
      <TextInput
        style={{ height: 40, borderColor: 'gray', borderWidth: 1, width: '80%', margin: 10, padding: 5 }}
        placeholder="Enter your email"
        onChangeText={text => setEmail(text)}
        value={email}
        keyboardType="email-address"
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

export default PasswordRecovery;