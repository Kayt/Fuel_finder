import unittest 
import fuel.bot

result1 = [["Fuel Station: "+data[0] + "\n" + "Fuel Type: " +data[2] + "\n"  + "Queue Length: " + data[4] + "\n" + "Location: " + data[5]+ " "+data[6] + "\n"],
           ["Fuel Station: "+data[0] + "\n" + "Fuel Type: " +data[2] + "\n"  + "Queue Length: " + data[4] + "\n" + "Location: " + data[5]+ " "+data[6] + "\n "],
           ["Fuel Station: "+data[0] + "\n" + "Fuel Type: " +data[2] + "\n"  + "Queue Length: " + data[4] + "\n" + "Location: " + data[5]+ " "+data[6] + "\n "],
           ["Fuel Station: "+data[0] + "\n" + "Fuel Type: " +data[2] + "\n"  + "Queue Length: " + data[4] + "\n" + "Location: " + data[5]+ " "+data[6] + "\n "]]

class BotTest(unittest.TestCase):
  def test_find_fuel(self):
    self.assertEqual(find_fuel('Mount Plesant', data), result1)
    self.assertEqual(find_fuel('Avondale', data), result2)
    self.assertEqual(find_fuel('Glendale', data), result3)
    self.assertEqual(find_fuel('Mkoba', data), result4)
    
    
    
    
  



