import React from 'react';
import { View, Text, Button, StyleSheet, Image } from 'react-native';

function LaunchPage({ navigation }) {
  return (
    <View style={styles.container}>
      <View style={styles.logoContainer}>
        <Image source={require('../../../assets/download.jpeg')} style={styles.logo} />
      </View>
      <Text style={styles.title}>Welcome to E-MAT</Text>
      <View style={styles.buttonContainer}>
        <Button
          title="Login"
          onPress={() => navigation.push("SignIn")}
          style={styles.button1}
        />
        </View>
        <Text style={styles.title1}>or</Text>
      <View style={styles.buttonContainer}>
        <Button
          title="Register"
          onPress={() => navigation.push("SignUp")}
          style={styles.button2}
        />
      </View>
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
  title1: {
    fontSize: 24,
    fontWeight: 'bold',
    margin:10
  },
  buttonContainer: {
    alignContent:"center",
    justifyContent:'center',
    width:150,

  },
  button1: {
    margin: 20,

  },
  button2: {
    margin: 20,
  },
});

export default LaunchPage;