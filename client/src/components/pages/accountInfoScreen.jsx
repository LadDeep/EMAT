import React, { useState } from 'react';
import { View, Text, Image, TextInput, Button, StyleSheet } from 'react-native';
import { Slider } from "react-native-ui-lib";

const AccountInfoScreen = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [monthlyBudget, setMonthlyBudget] = useState(10);
  const [alertValue, setAlertValue] = useState(0);

  const handleSave = () => {
    // TODO: Handle saving changes to account information
  }
 const handleMonthlyBudgetChange = (value) => {
    setMonthlyBudget(value);
    setAlertValue(value / 2);
  }

  const handleAlertValueChange = (val) => {
   setAlertValue(parseInt(val))
   console.log(parseInt(val))
  }


  return (
    <View style={styles.container}>
      <Image 
        source={require('../../../assets/download.jpeg')} 
        style={styles.profileImage} 
      />
      <Text style={styles.title}>Account Information</Text>
      <View style={styles.inputContainer}>
        <Text style={styles.label}>Name:</Text>
        <TextInput
          style={styles.input}
          value={name}
          onChangeText={setName}
          placeholder="Enter your name"
        />
      </View>
      <View style={styles.inputContainer}>
        <Text style={styles.label}>Email:</Text>
        <TextInput
          style={styles.input}
          value={email}
          onChangeText={setEmail}
          placeholder="Enter your email"
        />
      </View>
      <View style={styles.inputContainer}>
      <TextInput
       style={styles.input}
        keyboardType='numeric'
        placeholder='Monthly Budget'
        value={monthlyBudget}
        onChangeText={handleMonthlyBudgetChange}
      />
           <Slider
  minimumValue={0}
  maximumValue={monthlyBudget}
  onValueChange={(val) =>{handleAlertValueChange(val)} }
/>

      <Text style={styles.alertText}>Alert Value: {alertValue}</Text>
    </View>
      <Button title="Save" onPress={handleSave} />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'flex-start',
    padding: 16,
  },
  profileImage: {
    width: 150,
    height: 150,
    borderRadius: 75,
    marginBottom: 16,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 16,
  },
  inputContainer: {
    width: '100%',
    marginBottom: 16,
  },
  label: {
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 8,
  },
  input: {
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 4,
    padding: 8,
    fontSize: 16,
    width: '100%',
  },
});

export default AccountInfoScreen;
