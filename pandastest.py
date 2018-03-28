import pandas as pd

data = {'points': [{'curveNumber': 0, 'pointNumber': 1553, 'pointIndex': 1553, 'x': 468.8, 'y': 0.001025, 'text': 1012}, {'curveNumber': 0, 'pointNumber': 1554, 'pointIndex': 1554, 'x': 467.9, 'y': 0.00105, 'text': 1012.18}, {'curveNumber': 0, 'pointNumber': 1555, 'pointIndex': 1555, 'x': 467, 'y': 0.001075, 'text': 1012.36}, {'curveNumber': 0, 'pointNumber': 1556, 'pointIndex': 1556, 'x': 466.3, 'y': 0.00110833, 'text': 1012.54}, {'curveNumber': 0, 'pointNumber': 1557, 'pointIndex': 1557, 'x': 465.4, 'y': 0.00113333, 'text': 1012.72}, {'curveNumber': 0, 'pointNumber': 1558, 'pointIndex': 1558, 'x': 464.5, 'y': 0.00115833, 'text': 1012.9}, {'curveNumber': 0, 'pointNumber': 1559, 'pointIndex': 1559, 'x': 463.1, 'y': 0.00118333, 'text': 1013.08}, {'curveNumber': 0, 'pointNumber': 1560, 'pointIndex': 1560, 'x': 461.2, 'y': 0.00120833, 'text': 1013.26}, {'curveNumber': 0, 'pointNumber': 1561, 'pointIndex': 1561, 'x': 460.1, 'y': 0.00123333, 'text': 1013.44}, {'curveNumber': 0, 'pointNumber': 1562, 'pointIndex': 1562, 'x': 459.4, 'y': 0.00126667, 'text': 1013.62}, {'curveNumber': 0, 'pointNumber': 1563, 'pointIndex': 1563, 'x': 459, 'y': 0.00129167, 'text': 1013.8}, {'curveNumber': 0, 'pointNumber': 1564, 'pointIndex': 1564, 'x': 458.4, 'y': 0.001325, 'text': 1013.98}, {'curveNumber': 0, 'pointNumber': 1565, 'pointIndex': 1565, 'x': 457.4, 'y': 0.00135, 'text': 1014.16}, {'curveNumber': 0, 'pointNumber': 1566, 'pointIndex': 1566, 'x': 456.5, 'y': 0.00138333, 'text': 1014.34}, {'curveNumber': 0, 'pointNumber': 1567, 'pointIndex': 1567, 'x': 455.5, 'y': 0.00140833, 'text': 1014.52}, {'curveNumber': 0, 'pointNumber': 1568, 'pointIndex': 1568, 'x': 454.4, 'y': 0.00143333, 'text': 1014.7}, {'curveNumber': 0, 'pointNumber': 1569, 'pointIndex': 1569, 'x': 453.3, 'y': 0.00145833, 'text': 1014.88}, {'curveNumber': 0, 'pointNumber': 1570, 'pointIndex': 1570, 'x': 452.3, 'y': 0.00148333, 'text': 1015.06}, {'curveNumber': 0, 'pointNumber': 1571, 'pointIndex': 1571, 'x': 451.2, 'y': 0.00151667, 'text': 1015.24}, {'curveNumber': 0, 'pointNumber': 1572, 'pointIndex': 1572, 'x': 450, 'y': 0.00154167, 'text': 1015.42}, {'curveNumber': 0, 'pointNumber': 1573, 'pointIndex': 1573, 'x': 448.8, 'y': 0.00156667, 'text': 1015.6}, {'curveNumber': 0, 'pointNumber': 1574, 'pointIndex': 1574, 'x': 447.8, 'y': 0.00159167, 'text': 1015.78}, {'curveNumber': 0, 'pointNumber': 1575, 'pointIndex': 1575, 'x': 447, 'y': 0.00161667, 'text': 1015.96}, {'curveNumber': 0, 'pointNumber': 1576, 'pointIndex': 1576, 'x': 446, 'y': 0.00165, 'text': 1016.14}, {'curveNumber': 0, 'pointNumber': 1577, 'pointIndex': 1577, 'x': 444.7, 'y': 0.001675, 'text': 1016.32}, {'curveNumber': 0, 'pointNumber': 1578, 'pointIndex': 1578, 'x': 443.7, 'y': 0.00170833, 'text': 1016.5}, {'curveNumber': 0, 'pointNumber': 1579, 'pointIndex': 1579, 'x': 442.8, 'y': 0.00173333, 'text': 1016.68}, {'curveNumber': 0, 'pointNumber': 1580, 'pointIndex': 1580, 'x': 441.8, 'y': 0.00176667, 'text': 1016.86}, {'curveNumber': 0, 'pointNumber': 1581, 'pointIndex': 1581, 'x': 441, 'y': 0.00179167, 'text': 1017.04}, {'curveNumber': 0, 'pointNumber': 1582, 'pointIndex': 1582, 'x': 440.1, 'y': 0.001825, 'text': 1017.22}, {'curveNumber': 0, 'pointNumber': 1583, 'pointIndex': 1583, 'x': 438.9, 'y': 0.00185, 'text': 1017.4}, {'curveNumber': 0, 'pointNumber': 1584, 'pointIndex': 1584, 'x': 437.7, 'y': 0.00188333, 'text': 1017.58}, {'curveNumber': 0, 'pointNumber': 1585, 'pointIndex': 1585, 'x': 436.5, 'y': 0.00191667, 'text': 1017.76}, {'curveNumber': 0, 'pointNumber': 1586, 'pointIndex': 1586, 'x': 435.4, 'y': 0.00195, 'text': 1017.95}, {'curveNumber': 0, 'pointNumber': 1587, 'pointIndex': 1587, 'x': 434.6, 'y': 0.00198333, 'text': 1018.13}, {'curveNumber': 0, 'pointNumber': 1588, 'pointIndex': 1588, 'x': 433.5, 'y': 0.00200833, 'text': 1018.31}, {'curveNumber': 0, 'pointNumber': 1589, 'pointIndex': 1589, 'x': 432.3, 'y': 0.00203333, 'text': 1018.49}, {'curveNumber': 0, 'pointNumber': 1590, 'pointIndex': 1590, 'x': 431, 'y': 0.00205833, 'text': 1018.67}, {'curveNumber': 0, 'pointNumber': 1591, 'pointIndex': 1591, 'x': 430.1, 'y': 0.00209167, 'text': 1018.85}, {'curveNumber': 0, 'pointNumber': 1592, 'pointIndex': 1592, 'x': 429.3, 'y': 0.00211667, 'text': 1019.03}, {'curveNumber': 0, 'pointNumber': 1593, 'pointIndex': 1593, 'x': 428.2, 'y': 0.00214167, 'text': 1019.21}, {'curveNumber': 0, 'pointNumber': 1594, 'pointIndex': 1594, 'x': 426.9, 'y': 0.00215833, 'text': 1019.39}, {'curveNumber': 0, 'pointNumber': 1595, 'pointIndex': 1595, 'x': 425.6, 'y': 0.00218333, 'text': 1019.57}, {'curveNumber': 0, 'pointNumber': 1596, 'pointIndex': 1596, 'x': 424, 'y': 0.0022, 'text': 1019.75}, {'curveNumber': 0, 'pointNumber': 1597, 'pointIndex': 1597, 'x': 422.7, 'y': 0.002225, 'text': 1019.93}, {'curveNumber': 0, 'pointNumber': 1598, 'pointIndex': 1598, 'x': 421.7, 'y': 0.00224167, 'text': 1020.11}, {'curveNumber': 0, 'pointNumber': 1599, 'pointIndex': 1599, 'x': 420.5, 'y': 0.00225833, 'text': 1020.29}, {'curveNumber': 0, 'pointNumber': 1600, 'pointIndex': 1600, 'x': 419.2, 'y': 0.002275, 'text': 1020.47}, {'curveNumber': 0, 'pointNumber': 1601, 'pointIndex': 1601, 'x': 418, 'y': 0.00228333, 'text': 1020.65}, {'curveNumber': 0, 'pointNumber': 1602, 'pointIndex': 1602, 'x': 417, 'y': 0.0023, 'text': 1020.83}, {'curveNumber': 0, 'pointNumber': 1603, 'pointIndex': 1603, 'x': 416, 'y': 0.00230833, 'text': 1021.01}, {'curveNumber': 0, 'pointNumber': 1604, 'pointIndex': 1604, 'x': 414.8, 'y': 0.002325, 'text': 1021.19}, {'curveNumber': 0, 'pointNumber': 1605, 'pointIndex': 1605, 'x': 413.7, 'y': 0.00234167, 'text': 1021.37}, {'curveNumber': 0, 'pointNumber': 1606, 'pointIndex': 1606, 'x': 412.8, 'y': 0.00235, 'text': 1021.55}, {'curveNumber': 0, 'pointNumber': 1607, 'pointIndex': 1607, 'x': 411.7, 'y': 0.00235833, 'text': 1021.73}, {'curveNumber': 0, 'pointNumber': 1608, 'pointIndex': 1608, 'x': 410.7, 'y': 0.00236667, 'text': 1021.91}, {'curveNumber': 0, 'pointNumber': 1609, 'pointIndex': 1609, 'x': 409.7, 'y': 0.002375, 'text': 1022.09}, {'curveNumber': 0, 'pointNumber': 1610, 'pointIndex': 1610, 'x': 408.8, 'y': 0.00239167, 'text': 1022.27}, {'curveNumber': 0, 'pointNumber': 1611, 'pointIndex': 1611, 'x': 408.1, 'y': 0.00239167, 'text': 1022.45}, {'curveNumber': 0, 'pointNumber': 1612, 'pointIndex': 1612, 'x': 407.1, 'y': 0.0024, 'text': 1022.63}, {'curveNumber': 0, 'pointNumber': 1613, 'pointIndex': 1613, 'x': 406.2, 'y': 0.00240833, 'text': 1022.81}, {'curveNumber': 0, 'pointNumber': 1614, 'pointIndex': 1614, 'x': 405.2, 'y': 0.00241667, 'text': 1022.99}, {'curveNumber': 0, 'pointNumber': 1615, 'pointIndex': 1615, 'x': 404.3, 'y': 0.002425, 'text': 1023.17}, {'curveNumber': 0, 'pointNumber': 1616, 'pointIndex': 1616, 'x': 403.5, 'y': 0.002425, 'text': 1023.35}, {'curveNumber': 0, 'pointNumber': 1617, 'pointIndex': 1617, 'x': 402.5, 'y': 0.00243333, 'text': 1023.53}, {'curveNumber': 0, 'pointNumber': 1618, 'pointIndex': 1618, 'x': 401.6, 'y': 0.00243333, 'text': 1023.71}, {'curveNumber': 0, 'pointNumber': 1619, 'pointIndex': 1619, 'x': 400.8, 'y': 0.00244167, 'text': 1023.89}, {'curveNumber': 0, 'pointNumber': 1620, 'pointIndex': 1620, 'x': 400.1, 'y': 0.00244167, 'text': 1024.07}, {'curveNumber': 0, 'pointNumber': 1621, 'pointIndex': 1621, 'x': 399.1, 'y': 0.00244167, 'text': 1024.25}, {'curveNumber': 0, 'pointNumber': 1622, 'pointIndex': 1622, 'x': 398.3, 'y': 0.00244167, 'text': 1024.43}, {'curveNumber': 0, 'pointNumber': 1623, 'pointIndex': 1623, 'x': 397.5, 'y': 0.00244167, 'text': 1024.61}, {'curveNumber': 0, 'pointNumber': 1624, 'pointIndex': 1624, 'x': 396.6, 'y': 0.00245, 'text': 1024.79}, {'curveNumber': 0, 'pointNumber': 1625, 'pointIndex': 1625, 'x': 395.7, 'y': 0.00245, 'text': 1024.97}, {'curveNumber': 0, 'pointNumber': 1626, 'pointIndex': 1626, 'x': 395, 'y': 0.00245, 'text': 1025.15}, {'curveNumber': 0, 'pointNumber': 1627, 'pointIndex': 1627, 'x': 394, 'y': 0.00245, 'text': 1025.33}, {'curveNumber': 0, 'pointNumber': 1628, 'pointIndex': 1628, 'x': 393.2, 'y': 0.00245, 'text': 1025.51}, {'curveNumber': 0, 'pointNumber': 1629, 'pointIndex': 1629, 'x': 392.4, 'y': 0.00245, 'text': 1025.69}, {'curveNumber': 0, 'pointNumber': 1630, 'pointIndex': 1630, 'x': 391.4, 'y': 0.00245, 'text': 1025.87}, {'curveNumber': 0, 'pointNumber': 1631, 'pointIndex': 1631, 'x': 390.1, 'y': 0.00244167, 'text': 1026.05}, {'curveNumber': 0, 'pointNumber': 1632, 'pointIndex': 1632, 'x': 389.3, 'y': 0.00244167, 'text': 1026.23}, {'curveNumber': 0, 'pointNumber': 1633, 'pointIndex': 1633, 'x': 388.5, 'y': 0.00244167, 'text': 1026.41}, {'curveNumber': 0, 'pointNumber': 1634, 'pointIndex': 1634, 'x': 387.6, 'y': 0.00244167, 'text': 1026.59}, {'curveNumber': 0, 'pointNumber': 1635, 'pointIndex': 1635, 'x': 386.6, 'y': 0.00243333, 'text': 1026.77}, {'curveNumber': 0, 'pointNumber': 1636, 'pointIndex': 1636, 'x': 385.5, 'y': 0.00243333, 'text': 1026.95}, {'curveNumber': 0, 'pointNumber': 1637, 'pointIndex': 1637, 'x': 384.5, 'y': 0.002425, 'text': 1027.13}, {'curveNumber': 0, 'pointNumber': 1638, 'pointIndex': 1638, 'x': 383.7, 'y': 0.002425, 'text': 1027.31}, {'curveNumber': 0, 'pointNumber': 1639, 'pointIndex': 1639, 'x': 382.9, 'y': 0.002425, 'text': 1027.49}, {'curveNumber': 0, 'pointNumber': 1640, 'pointIndex': 1640, 'x': 382, 'y': 0.002425, 'text': 1027.67}, {'curveNumber': 0, 'pointNumber': 1641, 'pointIndex': 1641, 'x': 381, 'y': 0.00241667, 'text': 1027.85}, {'curveNumber': 0, 'pointNumber': 1642, 'pointIndex': 1642, 'x': 380.1, 'y': 0.00241667, 'text': 1028.03}, {'curveNumber': 0, 'pointNumber': 1643, 'pointIndex': 1643, 'x': 379.1, 'y': 0.00240833, 'text': 1028.21}, {'curveNumber': 0, 'pointNumber': 1644, 'pointIndex': 1644, 'x': 378.1, 'y': 0.0024, 'text': 1028.4}, {'curveNumber': 0, 'pointNumber': 1645, 'pointIndex': 1645, 'x': 377, 'y': 0.0024, 'text': 1028.57}, {'curveNumber': 0, 'pointNumber': 1646, 'pointIndex': 1646, 'x': 376, 'y': 0.00239167, 'text': 1028.75}, {'curveNumber': 0, 'pointNumber': 1647, 'pointIndex': 1647, 'x': 375.2, 'y': 0.00239167, 'text': 1028.94}, {'curveNumber': 0, 'pointNumber': 1648, 'pointIndex': 1648, 'x': 374.2, 'y': 0.00238333, 'text': 1029.11}, {'curveNumber': 0, 'pointNumber': 1649, 'pointIndex': 1649, 'x': 373, 'y': 0.00238333, 'text': 1029.29}, {'curveNumber': 0, 'pointNumber': 1650, 'pointIndex': 1650, 'x': 371.8, 'y': 0.002375, 'text': 1029.47}, {'curveNumber': 0, 'pointNumber': 1651, 'pointIndex': 1651, 'x': 370.7, 'y': 0.00236667, 'text': 1029.65}, {'curveNumber': 0, 'pointNumber': 1652, 'pointIndex': 1652, 'x': 369.8, 'y': 0.00235833, 'text': 1029.83}, {'curveNumber': 0, 'pointNumber': 1653, 'pointIndex': 1653, 'x': 369, 'y': 0.00235, 'text': 1030.01}, {'curveNumber': 0, 'pointNumber': 1654, 'pointIndex': 1654, 'x': 368.3, 'y': 0.00235, 'text': 1030.19}, {'curveNumber': 0, 'pointNumber': 1655, 'pointIndex': 1655, 'x': 367.1, 'y': 0.00234167, 'text': 1030.37}, {'curveNumber': 0, 'pointNumber': 1656, 'pointIndex': 1656, 'x': 366.2, 'y': 0.00233333, 'text': 1030.55}, {'curveNumber': 0, 'pointNumber': 1657, 'pointIndex': 1657, 'x': 365.1, 'y': 0.002325, 'text': 1030.73}, {'curveNumber': 0, 'pointNumber': 1658, 'pointIndex': 1658, 'x': 363.9, 'y': 0.00231667, 'text': 1030.91}, {'curveNumber': 0, 'pointNumber': 1659, 'pointIndex': 1659, 'x': 362.8, 'y': 0.00231667, 'text': 1031.09}, {'curveNumber': 0, 'pointNumber': 1660, 'pointIndex': 1660, 'x': 361.7, 'y': 0.00230833, 'text': 1031.27}, {'curveNumber': 0, 'pointNumber': 1661, 'pointIndex': 1661, 'x': 360.6, 'y': 0.0023, 'text': 1031.45}, {'curveNumber': 0, 'pointNumber': 1662, 'pointIndex': 1662, 'x': 359.9, 'y': 0.00229167, 'text': 1031.63}, {'curveNumber': 0, 'pointNumber': 1663, 'pointIndex': 1663, 'x': 359.1, 'y': 0.00228333, 'text': 1031.81}, {'curveNumber': 0, 'pointNumber': 1664, 'pointIndex': 1664, 'x': 358.1, 'y': 0.002275, 'text': 1031.99}, {'curveNumber': 0, 'pointNumber': 1665, 'pointIndex': 1665, 'x': 357.2, 'y': 0.002275, 'text': 1032.17}, {'curveNumber': 0, 'pointNumber': 1666, 'pointIndex': 1666, 'x': 356.2, 'y': 0.00226667, 'text': 1032.35}, {'curveNumber': 0, 'pointNumber': 1667, 'pointIndex': 1667, 'x': 355.2, 'y': 0.00225833, 'text': 1032.53}, {'curveNumber': 0, 'pointNumber': 1668, 'pointIndex': 1668, 'x': 354.2, 'y': 0.00225, 'text': 1032.71}, {'curveNumber': 0, 'pointNumber': 1669, 'pointIndex': 1669, 'x': 353.2, 'y': 0.00224167, 'text': 1032.89}], 'range': {'x': [353.1449140569814, 469.49904638568404], 'y': [0.0007670708598726123, 0.0030072697133757967]}}

df = pd.DataFrame.from_dict(data['points'], orient='columns')

print(df)