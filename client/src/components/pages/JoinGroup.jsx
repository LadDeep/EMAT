import React, { useState } from 'react';
import { View, Text, TextInput, Button, Alert,StyleSheet } from 'react-native';
import {JoinGroupApi} from '../../api/api';
import { useNavigation } from "@react-navigation/native";
function JoinGroup() {
  const [code, setCode] = useState('');
  const navigation = useNavigation();
  const handleValidation = () => {
   
    if (!code) {
      Alert.alert("",'Enter Some Value');
      return;
    }
    handleSubmit();
  };

  const handleSubmit = () => {
    // Code to send 
    console.log(code)
    JoinGroupApi(code,(response)=>{
        if(response.data.status){
            Alert.alert("",'Group Joined');
            navigation.push("GroupsTab")
        }
    },(err)=>{
        console.log(err)
    })
    
  };

  return (
    <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
      <Text style={styles.passwordRecoveryText}>Join Group</Text>
      <TextInput
        style={{ height: 40, borderColor: 'gray', borderWidth: 1, width: '80%', margin: 10,padding:5 }}
        placeholder="Enter your code"
        onChangeText={text => setCode(text)}
        value={code}
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

export default JoinGroup;