import React from 'react';
import { View, Text, StyleSheet, Image, TouchableOpacity } from 'react-native';

const accountDetails = () => {
  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Image
          style={styles.avatar}
          source={require('../../../assets/download.jpeg')} 
        />
        <View style={styles.userDetails}>
        <Text style={styles.name}>John Doe</Text>
        <Text style={styles.value}>johndoe@example.com</Text>

        </View>
        <TouchableOpacity style={styles.editButton}>
          <Text style={styles.editButtonText}>Edit</Text>
        </TouchableOpacity>
      </View>
      <View style={styles.details}>
      <View style={styles.heading}>
        <Text style={styles.headingText}>Expense Tracking</Text>
      </View>

        <View style={styles.row}>
        <Image
          style={styles.smallLogo}
          source={require('../../../assets/download.jpeg')} 
        />
          <Text style={styles.value1}>Preference</Text>
        </View>
        <View style={styles.row}>
        <Image
          style={styles.smallLogo}
          source={require('../../../assets/download.jpeg')} 
        />
          <Text style={styles.value1}>Expense Summary</Text>
        </View>
      </View>
      <View style={styles.details}>
      <View style={styles.heading}>
        <Text style={styles.headingText}>General</Text>
      </View>

        <View style={styles.row}>
        <Image
          style={styles.smallLogo}
          source={require('../../../assets/download.jpeg')} 
        />
          <Text style={styles.value1}>Contact E-Mat</Text>
        </View>
        <View style={styles.row}>
        <Image
          style={styles.smallLogo}
          source={require('../../../assets/download.jpeg')} 
        />
          <Text style={styles.value1}>Rate Us</Text>
        </View>
      </View>
      <TouchableOpacity style={styles.logoutButton}>
        <Text style={styles.logoutButtonText}>Logout</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    padding: 20,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 30,
    padding:6,
  },

  avatar: {
    width: 80,
    height: 80,
    borderRadius: 40,
    marginRight: 20, 
  },
  value: {
    flex: 1,
  },
  
  name: {
    fontSize: 24,
    fontWeight: 'bold',
    flex: 1,
  
  },
  editButton: {
    backgroundColor: '#eee',
    paddingVertical: 10,
    paddingHorizontal: 20,
    borderRadius: 5,
  
    marginLeft: 20,
  },
  editButtonText: {
    fontSize: 16,
  },
  userDetails:{
    flexDirection:'column',

  },
  details: {
    marginBottom: 30,
    
  },

  heading:{
    marginBottom:15
},
  headingText:{
    fontWeight: 'bold',
    fontSize:25,
  },
  label: {
    fontWeight: 'bold',
    width: 80, 
  },
  row: {
    flexDirection: 'row',
    marginBottom: 10,
    alignItems:'center'
  },
  smallLogo:{
    width: 40,
    height: 40,
    borderRadius: 40,
    marginRight: 20, 
},

  value1: {
    fontSize:17,
  },
  logoutButton: {
    backgroundColor: '#ff5733',
    paddingVertical: 10,
    paddingHorizontal: 20,
    borderRadius: 5,
    alignItems: 'center',
  },
  logoutButtonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
  },
});

export default accountDetails;