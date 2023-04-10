import React from 'react';
import { Dimensions, StyleSheet, View } from 'react-native';
import { BarChart, ProgressChart } from 'react-native-chart-kit';
import { Text, Card } from 'react-native-ui-lib';

const screenWidth = Dimensions.get('window').width;

const chartConfig = {
  backgroundGradientFrom: '#1E1E1E',
  backgroundGradientFromOpacity: 1,
  backgroundGradientTo: '#1E1E1E',
  backgroundGradientToOpacity: 1,
  color: (opacity = 1) => `rgba(255, 255, 255, ${opacity})`,
  strokeWidth: 2,
  barPercentage: 0.5,
  useShadowColorFromDataset: false,
};

const primaryColor = '#E44343';
const secondaryColor = '#27AE60';

const ChartDisplay = () => {
  const data = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    datasets: [
      {
        data: [50, 45, 28, 80, 99, 43, 89, 55, 67, 87, 23, 34],
      },
    ],
  };
  const data1 = {
    labels: ["Monthly Spending", "Monthly Budget", "Monthly Lending"],
    data: [0.4, 0.6, 0.8]
  };

  return (
    <View style={styles.container}>
      <View style={styles.cardContainer}>
        <Card style={[styles.card, { backgroundColor: primaryColor }]}>
          <Text white>Spending</Text>
          <Text white>$120</Text>
        </Card>
        <Card style={[styles.card, { backgroundColor: secondaryColor }]}>
          <Text white>Lending</Text>
          <Text white>$140</Text>
        </Card>
      </View>
      <View style={styles.pieChartContainer}>

        <ProgressChart
          data={data1}
          width={screenWidth}
          height={220}
          strokeWidth={16}
          radius={32}
          chartConfig={chartConfig}
          hideLegend={false}
        />
      </View>
      <View style={styles.chartContainer}>
        <Text h4 white>
          Spending Chart
        </Text>
        <BarChart
          data={data}
          width={screenWidth}
          height={220}
          yAxisLabel="$"
          chartConfig={chartConfig}
        />
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    paddingTop: 45,
    flex: 1,
    backgroundColor: '#1E1E1E',
  },
  cardContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingHorizontal: 20,
    paddingTop: 20,
  },
  card: {
    width: '47%',
    height: 80,
    borderRadius: 10,
    justifyContent: 'center',
    alignItems: 'center',
  },
  pieChartContainer: {
    marginTop: 20,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    paddingRight: 15,

  },
  chartContainer: {
    marginTop: 20,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    paddingRight: 15,
  },
});

export default ChartDisplay;
