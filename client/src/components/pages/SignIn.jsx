import React, { useState } from "react";
import { LoginUser } from "../../api/api";
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  Image,
  ActivityIndicator,
} from "react-native";
import { save } from "../../secureStore";

const SignIn = ({ navigation, route }) => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const {handleLogin} = route.params
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSignIn = () => {
  let payload={
    email:email,
    password:password
  }
  console.log("This is my payload",payload);
  setError(null)
  LoginUser(
    payload,
    async (res) => {
     console.log("This is response of registered user",res)
     if(res.data.status){
       await save("ACCESS_TOKEN", res.data.access_token)
       await save("USER_ID", res.data.user_id)
      handleLogin()
      } else {
        setError(res.data.message)
      }
        },
        (err) => {
          console.log(err);
      setError(err.response.data.error)
        }
      );
    setIsLoading(false);
  };

  return (
    <View style={styles.container}>
    <Image style={styles.img} source={require('../../../assets/download.jpeg')} />
      <Text style={styles.title}>Welcome to E-Mat</Text>
      <TextInput
        style={styles.input}
        placeholder="Email"
        onChangeText={(text) => setEmail(text)}
        value={email}
        autoCapitalize="none"
        autoComplete="email"
        textContentType="emailAddress"
        keyboardType="email-address"
        activeUnderlineColor="blue"
      />
      <TextInput
        style={styles.input}
        placeholder="Password"
        onChangeText={(text) => setPassword(text)}
        value={password}
        secureTextEntry
      />
      <TouchableOpacity
        style={styles.button}
        onPress={() => {
          setIsLoading(true);
          handleSignIn();
        }}
      >
        <Text style={styles.buttonText}>Login</Text>
      </TouchableOpacity>
      <Text onPress={() => navigation.push("PasswordRecovery")}>
        Forgot Password?
      </Text>
      {isLoading && <ActivityIndicator size="large" color="blue" />}
      {error && <Text style={styles.error}>{error}</Text>}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
    backgroundColor:'F7F7F2',
  },
  img:{
    width:90,
    height:90,
    marginBottom:40,
  },
  title: {
    fontSize: 24,
    marginBottom: 16,
  },
  input: {
    width: "80%",
    height: 40,
    borderWidth: 1,
    borderColor: "gray",
    padding: 8,
    marginBottom: 16,
  },
  button: {
    backgroundColor: "blue",
    padding: 12,
    width: "80%",
  },
  buttonText: {
    color: "white",
    fontSize: 18,
    textAlign: "center",
  },
  error: {
    color: "red",
  }
});

export default SignIn;
