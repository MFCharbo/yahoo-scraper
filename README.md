# yahoo-scraper


MySQL queries & Related Info (can also be found in streamSQL.py)
## Related Info
user: root
password: (leave blank)

## Queries
CREATE DATABASE `Finance` /*!40100 DEFAULT CHARACTER SET latin1 */;

CREATE TABLE `stockActions` (
  `date` date NOT NULL,
  `company` varchar(10) NOT NULL,
  `action` varchar(45) DEFAULT NULL,
  `ratio` float DEFAULT NULL,
  PRIMARY KEY (`date`,`company`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `stocks` (
  `date` date NOT NULL,
  `open` float DEFAULT NULL,
  `high` float DEFAULT NULL,
  `low` float DEFAULT NULL,
  `close` float DEFAULT NULL,
  `adj_close` float DEFAULT NULL,
  `volume` int(11) DEFAULT NULL,
  `company` varchar(45) NOT NULL,
  PRIMARY KEY (`date`,`company`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
