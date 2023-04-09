import { useNavigation } from '@react-navigation/native';
import React, { useState } from 'react';
import { View, Text, TextInput, Button, StyleSheet, Image } from 'react-native';
import { UpdatePassword } from '../api/api';

function PasswordReset({ route }) {
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const navigation = useNavigation();
  const { token } = route.params
  const handleResetPassword = () => {
    if (password !== confirmPassword) {
      alert('Passwords do not match');
      return;
    }

    // Code to reset password
    console.log("TOKEN++++++", token);
    console.log("PASWORD", password)
    let payload = { password: password }
    UpdatePassword(token, payload,
      (res) => {
        console.log("Response From Updated Paassword", res.data)
        navigation.navigate("SignIn")

      }, (err) => {
        console.log("err", err)
      });
    alert('Password has been reset');
  };

  return (
    <View style={styles.container}>
      <View style={styles.logoContainer}>
        <Image source={require('../../assets/download.jpeg')} style={styles.logo} />
      </View>
      <Text style={styles.title}>Password Reset</Text>
      <TextInput
        style={styles.input}
        placeholder="New Password"
        secureTextEntry={true}
        onChangeText={text => setPassword(text)}
        value={password}
      />
      <TextInput
        style={styles.input}
        placeholder="Confirm Password"
        secureTextEntry={true}
        onChangeText={text => setConfirmPassword(text)}
        value={confirmPassword}
      />
      <Button
        title="Reset Password"
        onPress={handleResetPassword}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },
  logoContainer: {
    alignItems: 'center',
    marginBottom: 20,
  },
  logo: {
    width: 100,
    height: 100,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
  },
  input: {
    height: 40,
    borderColor: 'gray',
    borderWidth: 1,
    width: '80%',
    margin: 10,
    paddingHorizontal: 10,
  },
});

export default PasswordReset;