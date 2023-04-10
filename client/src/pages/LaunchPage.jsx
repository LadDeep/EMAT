import React from 'react';
import { Text, StyleSheet, Image } from 'react-native';
import {View, Button } from 'react-native-ui-lib';

function LaunchPage({ navigation }) {
  return (
    <View flex center>
        <Image source={require('../../assets/pict--expenses-calculation-management.png')} style={styles.logo} />
      <Text style={styles.title}>Welcome to E-MAT</Text>
        <Button
          label="Login"
          onPress={() => navigation.push("SignIn")}
          style={styles.button}
        />
        <Text style={styles.title1}>or</Text>
        <Button
          label="Register"
          onPress={() => navigation.push("SignUp")}
          style={styles.button}
          />
    </View>
  );
}

const styles = StyleSheet.create({
  logo: {
    width: 100,
    height: 100,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
  },
  title1: {
    fontSize: 24,
    fontWeight: 'bold',
    margin:10
  },
  button: {
    backgroundColor: "blue",
    width: "50%",
  },
});

export default LaunchPage;