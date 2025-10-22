-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Host: apt.db
-- Generation Time: Oct 17, 2025 at 12:24 PM
-- Server version: 10.6.17-MariaDB-1:10.6.17+maria~ubu2004
-- PHP Version: 8.3.24-nfsn1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `invoiceplane`
--

-- --------------------------------------------------------

--
-- Table structure for table `ip_clients`
--

CREATE TABLE `ip_clients` (
  `client_id` int(11) NOT NULL,
  `client_date_created` datetime NOT NULL,
  `client_date_modified` datetime NOT NULL,
  `client_name` text DEFAULT NULL,
  `client_address_1` text DEFAULT NULL,
  `client_address_2` text DEFAULT NULL,
  `client_city` text DEFAULT NULL,
  `client_state` text DEFAULT NULL,
  `client_zip` text DEFAULT NULL,
  `client_country` text DEFAULT NULL,
  `client_phone` text DEFAULT NULL,
  `client_fax` text DEFAULT NULL,
  `client_mobile` text DEFAULT NULL,
  `client_email` text DEFAULT NULL,
  `client_web` text DEFAULT NULL,
  `client_vat_id` text DEFAULT NULL,
  `client_tax_code` text DEFAULT NULL,
  `client_language` varchar(255) DEFAULT 'system',
  `client_active` int(1) NOT NULL DEFAULT 1,
  `client_surname` varchar(255) DEFAULT NULL,
  `client_avs` varchar(16) DEFAULT NULL,
  `client_insurednumber` varchar(30) DEFAULT NULL,
  `client_veka` varchar(30) DEFAULT NULL,
  `client_birthdate` date DEFAULT NULL,
  `client_gender` int(1) DEFAULT 0
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `ip_clients`
--

INSERT INTO `ip_clients` (`client_id`, `client_date_created`, `client_date_modified`, `client_name`, `client_address_1`, `client_address_2`, `client_city`, `client_state`, `client_zip`, `client_country`, `client_phone`, `client_fax`, `client_mobile`, `client_email`, `client_web`, `client_vat_id`, `client_tax_code`, `client_language`, `client_active`, `client_surname`, `client_avs`, `client_insurednumber`, `client_veka`, `client_birthdate`, `client_gender`) VALUES
(1, '2022-12-13 07:36:23', '2024-03-08 12:19:29', 'Paul', '11 Thompson St', 'Ascot', 'Perth', 'WA', '6104', 'AU', '', '', '0401568828', 'paul@caston.id.au', 'http://paul.caston.id.au', '', '', 'system', 1, 'Caston', NULL, NULL, NULL, '0000-00-00', 0),
(2, '2023-01-08 02:59:21', '2023-01-08 04:16:55', 'Compton Burgers', '196 Stirling St', '', 'Perth', 'WA', '6000', 'AU', '(08) 9328 3858', '', '0415 154 102', 'comptonburgers@outlook.com', 'https://comptonburgers.com.au/', '', '', 'system', 1, '', NULL, NULL, NULL, '0000-00-00', 0),
(3, '2023-02-01 07:16:52', '2023-02-01 07:17:37', 'Steve', '9 Amity Blvd Coogee', '', 'Perth', 'WA', '6104', 'AU', '', '', '0458790159', 'stevewells55@yahoo.com.au', '', '', '', 'system', 1, 'Wells', NULL, NULL, NULL, '0000-00-00', 0),
(4, '2023-04-29 21:44:27', '2023-04-30 00:11:50', 'Malcolm', '99 Wordsworth Avenue', 'Yokine', 'Perth', 'WA', '6060', 'AU', '', '', '0419 958 706', '', '', '', '', 'system', 1, 'Sandman', NULL, NULL, NULL, '0000-00-00', 0),
(5, '2023-05-02 10:28:59', '2023-05-02 10:28:59', 'Daniel', '', '', '', '', '', '', '', '', '+44 7857 147620', 'daniel@flashware.net', '', '', '', 'system', 1, 'Pearson', NULL, NULL, NULL, '0000-00-00', 0),
(6, '2023-05-09 10:57:37', '2023-05-09 10:58:12', 'Robert Boykett', '81a Robinson Ave Belmont', '', 'Perth', 'WA', '6104', 'AU', '', '', '0411 840 726 ', 'sales@portseafurnishings.com.au ', 'https://www.portseafurnishings.com.au/', '', '', 'system', 1, '', NULL, NULL, NULL, '0000-00-00', 0),
(7, '2023-05-22 06:24:24', '2024-03-08 02:54:12', 'Olena', '9 Brian Ave Yokine', '', 'Perth', 'WA', '6060', 'AU', '', '', '0411 440 598', 'olenacas2@gmail.com', '', '', '', 'system', 1, '', NULL, NULL, NULL, '0000-00-00', 1),
(8, '2023-05-23 02:33:22', '2025-06-24 05:06:06', 'Leah', '2424 Great Northern Hwy', 'Bullsbrook', 'Perth', 'WA', '6084', 'AU', '0411149090', '', '', 'leah@mrssheen.com.au', '', '', '', 'system', 1, 'McIntosh', NULL, NULL, NULL, '0000-00-00', 1),
(9, '2023-05-28 01:14:11', '2023-05-28 01:14:11', 'Anita', '126 Westswan Road', ' BASSENDEAN', 'Perth', 'WA', '6054', 'AU', '', '', '0417 090 039', 'accounts@primelineplumbing.com.au', 'http://www.primelineplumbing.com.au', '', '', 'system', 1, 'Farrugia', NULL, NULL, NULL, '0000-00-00', 1),
(10, '2023-06-19 08:44:22', '2023-06-20 03:42:04', 'Stephen Clarkson', '97 Keymer St', 'Belmont', 'Perth', 'WA', '6104', '', '', '', '0439947722', 'stephen.1.clarkson@gmail.com', '', '', '', 'system', 1, '', NULL, NULL, NULL, '0000-00-00', 0),
(11, '2023-07-25 10:04:09', '2023-12-27 08:27:21', 'Noelle', '121 Watley Cres', 'Bayswater', 'Perth', 'WA', '6043', 'AU', '9271 9948', ' 0488872814', '0452246277', 'nrev1@hotmail.com', '', '', '', 'system', 1, 'Revera', NULL, NULL, NULL, '0000-00-00', 1),
(12, '2023-08-03 06:22:31', '2023-08-03 06:22:31', 'Ken', '68 Leake St', 'Bayswater', 'Perth', 'WA', '6104', 'AU', '(08) 9272 7162', '', '', '', '', '', '', 'system', 1, 'Cashmore', NULL, NULL, NULL, '0000-00-00', 0),
(13, '2023-09-14 09:34:17', '2024-05-06 10:27:20', 'Glenda', '50A Marchamley Street', 'Laithlain', 'Perth', 'WA', '6100', 'AU', '', '', '0458855553', 'glen@webshield.net.au', '', '', '', 'system', 1, 'Schipper', NULL, NULL, NULL, '0000-00-00', 0),
(14, '2023-09-18 08:47:10', '2023-09-18 08:59:32', 'Preet Chouhan', ' 10/267 Scarborough Beach Rd', 'Mount Hawthorn', 'Perth', 'WA', '6016', 'AU', ' (08) 6162 3758', '', '', 'sales@hockeyinternational.com.au', 'www.hockeyinternational.com.au', '', '', 'system', 1, 'Hockey International', NULL, NULL, NULL, '0000-00-00', 1),
(15, '2023-10-08 11:01:22', '2023-10-09 03:18:14', 'Kevin Young', 'Unit 8 / 51 Coode Street ', '', 'Perth', 'WA', '6104', 'AU', '', '', '0434620243', 'kpy123@gmail.com', '', '', '', 'system', 1, '', NULL, NULL, NULL, '0000-00-00', 0),
(16, '2023-12-20 02:13:22', '2023-12-20 02:13:22', 'Scott', '17 Hope Street Beechboro', '', 'Perth', 'WA', '6063', 'AU', '', '', '0447850246', '', '', '', '', 'system', 1, '', NULL, NULL, NULL, '0000-00-00', 0),
(17, '2023-12-20 08:43:30', '2023-12-20 08:43:30', 'Sue Rogowski', '127 Whitfield Street', 'Bassendean', 'Perth', 'WA', '6104', 'AU', '', '', '0426778624', '', '', '', '', 'system', 1, '', NULL, NULL, NULL, '0000-00-00', 1),
(18, '2023-12-22 09:59:27', '2024-04-14 10:54:01', 'Paul Samuel', '5/18 Angove St', 'North Perth', 'Perth', 'WA', '6006', '', '', '', '0401080886', 'paul@statepropertyadvisory.com.au', '', '', '', 'system', 1, '', NULL, NULL, NULL, '0000-00-00', 0),
(19, '2023-12-28 01:13:47', '2023-12-28 01:13:47', 'Ashley Bell', '3/36 Devon Rd', 'Bassendean', 'Perth', 'WA', '6054', 'AU', '92796583', '', '', 'ashgate4u@gmail.com', '', '', '', 'system', 1, '', NULL, NULL, NULL, '0000-00-00', 0),
(20, '2023-12-28 02:11:52', '2023-12-28 02:11:52', 'Louise Joesbury ', '120 Kenny Street  WA', 'BASSENDEAN', 'Perth', 'WA', '6054', 'AU', '', '', '0408899875', 'ljoesbury1@optusnet.com.au', '', '', '', 'system', 1, '', NULL, NULL, NULL, '0000-00-00', 0),
(21, '2024-02-07 08:57:45', '2024-02-07 08:58:13', 'Sarah', 'level 7 105 St Georges Terrace', '', 'Perth', 'WA', '6000', '', '', '', '0418930144', '', '', '', '', 'system', 1, 'Ladybank holdings', NULL, NULL, NULL, '0000-00-00', 1),
(22, '2024-02-15 03:46:20', '2024-03-08 12:03:48', 'Steven', 'Unit 31 / 7th Floor', '105 St Georges terrace', 'Perth', 'WA', '6000', 'AU', '(08) 9481 4655', '', '0447 769 479', '', '', '', '', 'system', 1, 'Sparkman', NULL, NULL, NULL, '0000-00-00', 0),
(23, '2024-02-22 00:52:36', '2024-02-23 01:57:10', 'Jack Noordewier', '80 597 Kalamunda road Hillview Kalamunda', '', 'Perth', 'WA', '6076', 'AU', '', '', '0451168455', 'jacknn1932@gmail.com', '', '', '', 'system', 1, '', NULL, NULL, NULL, '0000-00-00', 0),
(24, '2024-02-29 05:46:48', '2024-02-29 06:00:58', 'Yvonne Cecil', '4 Vance Close', 'Kingsley', 'Perth', 'WA', '6026', 'AU', '', '', '0403179164', 'cecil6@bigpond.com', '', '', '', 'system', 1, '', NULL, NULL, NULL, '0000-00-00', 1),
(27, '2024-04-09 08:41:29', '2024-04-09 08:42:03', 'Keith', '6 Kenilworth Street', 'Maylands', 'Perth', 'WA', '6151', 'AU', '', '', '0415 295 811', '', '', '', '', 'system', 1, '', NULL, NULL, NULL, '0000-00-00', 0),
(25, '2024-03-06 21:31:59', '2024-03-06 21:31:59', 'Joe Bloggs', '123 Evergreen Terrace', 'Leederville', 'Perth', 'WA', '6007', 'AU', '', '', '', 'joe@blogs.com.au', '', '', '', 'system', 1, 'Business name Pty Ltd', NULL, NULL, NULL, '0000-00-00', 0),
(26, '2024-03-08 08:24:55', '2024-03-08 08:24:55', 'Georgie', 'house 120  597 Kalamunda Rd', 'Hillview lifestyle village High Wycombe ', 'Perth', 'WA', '6057', '', '', '', '0401313315', 'georgiew@buzzynet.net', '', '', '', 'system', 1, '', NULL, NULL, NULL, '0000-00-00', 0),
(28, '2024-05-10 08:43:14', '2025-02-11 01:26:35', 'Judith', '133 Second Avevue', 'Eden Hill', 'Perth', 'Wa', '6054', 'AU', '', '', '0498226376', 'judeelduke@gmail.com', '', '', '', 'system', 1, 'Elt', NULL, NULL, NULL, '0000-00-00', 0),
(29, '2024-05-22 01:27:46', '2024-05-22 01:27:46', 'Tony', '4 Boronia Court   ', 'MORLEY', 'Perth', 'WA', '6062', 'AU', '', '', '0407610329', '', '', '', '', 'system', 1, 'Mazella', NULL, NULL, NULL, '0000-00-00', 0),
(30, '2024-06-03 08:43:12', '2024-06-04 04:32:40', 'Mike', '102 Hillview lifestyle village', '597 Kalamunda Rd, High Wycombe WA ', 'Perth', 'WA', '6104', 'AU', '', '', '0486 005 858', 'mjboag@outlook.com', '', '', '', 'system', 1, 'Boag', NULL, NULL, NULL, '0000-00-00', 0),
(31, '2024-06-10 03:22:19', '2024-07-10 08:43:28', 'Paul', 'unit 266', '597 Kalamunda Rd, High Wycombe WA', 'Perth', 'WA', '6057', 'AU', '', '', '0419265041', 'p_piercy@bigpond.net.au', '', '', '', 'system', 1, 'Piercy', NULL, NULL, NULL, '0000-00-00', 0),
(32, '2024-06-11 05:28:50', '2024-06-11 10:25:18', 'Dudley', '95a Matthewson Raod', 'Ascot', 'Perth', 'WA', '6104', '', '', '', '0428115208', 'corbdj55@gmail.com', '', '', '', 'system', 1, 'Corbett', NULL, NULL, NULL, '0000-00-00', 0),
(33, '2024-06-16 05:50:40', '2024-06-16 05:50:40', 'Renee', '53 Stanton Road', 'Redcliffe', 'Perth', 'WA', '6104', '', '', '', '0435314154', 'renee.westrheim@gmail.com', '', '', '', 'system', 1, 'Westrheim', NULL, NULL, NULL, '0000-00-00', 0),
(34, '2024-06-17 07:15:08', '2024-06-17 07:15:08', 'Shirley ', '04/15 Claughton Way', 'BASSENDEAN', 'Perth', 'WA', '6054', 'AU', '', '', '0419 957 068', '', '', '', '', 'system', 1, 'Lance', NULL, NULL, NULL, '0000-00-00', 1),
(35, '2024-07-15 05:00:04', '2024-07-15 05:01:56', 'Simon', '', 'Bayswater', 'Perth', 'WA', '6053', 'AU', '', '', '0477017410', '', '', '', '', 'system', 1, '', NULL, NULL, NULL, '0000-00-00', 0),
(36, '2024-08-12 03:36:49', '2024-08-13 07:41:10', 'Andrea', 'PO BOX 338', '', 'Exmouth', 'WA', '6707', 'AU', '', '', '0417493705', 'amkiesey@bigpond.com', '', '', '', 'system', 1, 'Kitsey', NULL, NULL, NULL, '0000-00-00', 1),
(37, '2024-08-26 09:44:50', '2024-09-10 03:42:29', 'Neville Parnham', '10 Thompson St Ascot', '', 'Perth', 'WA', '6104', 'AU', '', '', '', 'npar9482@bigpond.net.au', '', '', '', 'system', 1, '', NULL, NULL, NULL, '0000-00-00', 0),
(38, '2024-09-13 02:28:59', '2024-09-13 07:58:26', 'Brian', '3 Watson St', 'BASSENDEAN', 'Perth', 'WA', '6054', 'AU', '', '', '0418943567', 'annette.joesbury@bigpond.com', '', '', '', 'system', 1, 'Joesbury', NULL, NULL, NULL, '0000-00-00', 0),
(39, '2024-09-30 08:47:36', '2024-09-30 08:47:36', 'Steve', 'Unit 1 16-18 Kelvin St', 'Maylands', 'Perth', 'WA', '6051', 'AU', '', '', '0422 716 409', 'stevehandford@gmail.com', '', '', '', 'system', 1, 'Handford', NULL, NULL, NULL, '0000-00-00', 0),
(40, '2024-11-05 08:30:04', '2024-11-05 08:30:04', 'Marian', '39/597 Kalamunda Rd', 'High Wycombe WA 6057', 'Perth', 'WA', '6057', 'AU', '08 6255 4720', '', '', '', '', '', '', 'system', 1, 'Willis', NULL, NULL, NULL, '0000-00-00', 0),
(41, '2024-12-02 03:17:46', '2024-12-02 03:17:46', 'Janice', '25 Milano Ave', 'Stirling', 'Perth', 'WA', '6021', 'AU', '', '', '0422 929 656', '', '', '', '', 'system', 1, '', NULL, NULL, NULL, '0000-00-00', 1),
(42, '2025-01-17 04:23:02', '2025-01-17 04:23:02', 'John Wiltshire', 'house 248 /597 ', 'Kalamunda Rd, High Wycombe', '', '', '', '', '', '', '0475599764', '', '', '', '', 'system', 1, '', NULL, NULL, NULL, '0000-00-00', 0),
(43, '2025-03-04 03:47:47', '2025-03-04 03:50:34', 'Gordon', '879 Albany Hwy', 'East Victoria Park', 'Perth', 'WA', '6101', '', '', '', '0438273629', 'thehavenincevp@hotmail.com', 'https://havenwellwebsite.wixsite.com/my-site-1/the-haven', '', '', 'system', 1, 'Sutherland', NULL, NULL, NULL, '0000-00-00', 0),
(44, '2025-05-22 06:22:38', '2025-05-23 02:18:22', 'Peter', '34 Floyd St Trigg', '', 'Perth', 'WA', '6029', 'AU', '', '', '0423317061', 'peterbs3008@gmail.com', '', '', '', 'system', 1, 'Shipway', NULL, NULL, NULL, '0000-00-00', 0),
(45, '2025-07-31 23:26:56', '2025-07-31 23:26:56', 'Duncan Cutbrush', '288 Great Eastern Hwy Ascot', '', 'Perth', 'WA', '6104', 'AU', '(08) 9479 4077', '', '0476 21 866', 'info@airportselfstorage.com.au', 'https://airportselfstorage.com.au/', '', '', 'system', 1, '', NULL, NULL, NULL, '0000-00-00', 0);

-- --------------------------------------------------------

--
-- Table structure for table `ip_client_custom`
--

CREATE TABLE `ip_client_custom` (
  `client_custom_id` int(11) NOT NULL,
  `client_id` int(11) NOT NULL,
  `client_custom_fieldid` int(11) NOT NULL,
  `client_custom_fieldvalue` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `ip_client_custom`
--

INSERT INTO `ip_client_custom` (`client_custom_id`, `client_id`, `client_custom_fieldid`, `client_custom_fieldvalue`) VALUES
(1, 2, 1, 'Compton Burgers'),
(2, 3, 1, NULL),
(3, 4, 1, NULL),
(4, 5, 1, 'Flashware Solutions'),
(5, 6, 1, 'Port Sea Furnishings'),
(6, 7, 1, NULL),
(7, 8, 1, 'Mrs Sheen Sparkle and Clean'),
(8, 9, 1, 'Prime Line Plumbing and Gas'),
(9, 10, 1, NULL),
(10, 11, 1, NULL),
(11, 12, 1, NULL),
(12, 13, 1, 'Home Safety Electrics'),
(13, 14, 1, 'Hockey International'),
(14, 15, 1, NULL),
(15, 16, 1, NULL),
(16, 17, 1, NULL),
(17, 18, 1, 'State Property Advisory'),
(18, 19, 1, NULL),
(19, 20, 1, NULL),
(20, 21, 1, 'Lady bank holdings'),
(21, 22, 1, 'Ladybank Holdings (WA) Pty Ltd'),
(22, 23, 1, NULL),
(23, 24, 1, NULL),
(24, 25, 1, NULL),
(25, 26, 1, NULL),
(26, 1, 1, 'SEN'),
(27, 27, 1, NULL),
(28, 28, 1, NULL),
(29, 29, 1, NULL),
(30, 30, 1, NULL),
(31, 31, 1, NULL),
(32, 32, 1, NULL),
(33, 33, 1, NULL),
(34, 34, 1, NULL),
(35, 35, 1, NULL),
(36, 36, 1, NULL),
(37, 37, 1, 'Parnham Racing'),
(38, 38, 1, NULL),
(39, 39, 1, NULL),
(40, 40, 1, NULL),
(41, 41, 1, NULL),
(42, 42, 1, NULL),
(43, 43, 1, 'The Haven Centre Inc'),
(44, 44, 1, NULL),
(45, 45, 1, 'Airport Self Storage');

-- --------------------------------------------------------

--
-- Table structure for table `ip_client_notes`
--

CREATE TABLE `ip_client_notes` (
  `client_note_id` int(11) NOT NULL,
  `client_id` int(11) NOT NULL,
  `client_note_date` date NOT NULL,
  `client_note` longtext NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `ip_client_notes`
--

INSERT INTO `ip_client_notes` (`client_note_id`, `client_id`, `client_note_date`, `client_note`) VALUES
(1, 12, '2023-08-03', 'Windows 10 desktop'),
(2, 17, '2023-12-20', 'Mac'),
(3, 11, '2024-01-15', 'Noelle mobile 0432 203 928'),
(4, 23, '2024-02-22', 'Near Forrest home drive'),
(5, 31, '2024-06-10', 'Dell keyboard with sticky keys'),
(6, 31, '2024-07-10', 'New Lenovo computer');

-- --------------------------------------------------------

--
-- Table structure for table `ip_custom_fields`
--

CREATE TABLE `ip_custom_fields` (
  `custom_field_id` int(11) NOT NULL,
  `custom_field_table` varchar(50) DEFAULT NULL,
  `custom_field_label` varchar(50) DEFAULT NULL,
  `custom_field_type` varchar(255) NOT NULL DEFAULT 'TEXT',
  `custom_field_location` int(11) DEFAULT 0,
  `custom_field_order` int(11) DEFAULT 999
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `ip_custom_fields`
--

INSERT INTO `ip_custom_fields` (`custom_field_id`, `custom_field_table`, `custom_field_label`, `custom_field_type`, `custom_field_location`, `custom_field_order`) VALUES
(1, 'ip_client_custom', 'Company Name', 'TEXT', 3, 1);

-- --------------------------------------------------------

--
-- Table structure for table `ip_custom_values`
--

CREATE TABLE `ip_custom_values` (
  `custom_values_id` int(11) NOT NULL,
  `custom_values_field` int(11) NOT NULL,
  `custom_values_value` text NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `ip_email_templates`
--

CREATE TABLE `ip_email_templates` (
  `email_template_id` int(11) NOT NULL,
  `email_template_title` text DEFAULT NULL,
  `email_template_type` varchar(255) DEFAULT NULL,
  `email_template_body` longtext NOT NULL,
  `email_template_subject` text DEFAULT NULL,
  `email_template_from_name` text DEFAULT NULL,
  `email_template_from_email` text DEFAULT NULL,
  `email_template_cc` text DEFAULT NULL,
  `email_template_bcc` text DEFAULT NULL,
  `email_template_pdf_template` varchar(255) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `ip_families`
--

CREATE TABLE `ip_families` (
  `family_id` int(11) NOT NULL,
  `family_name` text DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `ip_families`
--

INSERT INTO `ip_families` (`family_id`, `family_name`) VALUES
(1, 'service'),
(2, 'desktop parts'),
(3, 'Software'),
(4, 'accessories'),
(5, 'computer systems'),
(6, 'Monitors'),
(7, 'printers'),
(8, 'cables'),
(9, 'speakers'),
(10, 'External drives'),
(11, 'internal adapters'),
(12, 'nvme drives'),
(13, 'Networking'),
(14, 'Tablets'),
(15, 'Mini PCs'),
(16, 'laptop memory');

-- --------------------------------------------------------

--
-- Table structure for table `ip_imports`
--

CREATE TABLE `ip_imports` (
  `import_id` int(11) NOT NULL,
  `import_date` datetime NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `ip_import_details`
--

CREATE TABLE `ip_import_details` (
  `import_detail_id` int(11) NOT NULL,
  `import_id` int(11) NOT NULL,
  `import_lang_key` varchar(35) NOT NULL,
  `import_table_name` varchar(35) NOT NULL,
  `import_record_id` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `ip_invoices`
--

CREATE TABLE `ip_invoices` (
  `invoice_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `client_id` int(11) NOT NULL,
  `invoice_group_id` int(11) NOT NULL,
  `invoice_status_id` tinyint(2) NOT NULL DEFAULT 1,
  `is_read_only` tinyint(1) DEFAULT NULL,
  `invoice_password` varchar(90) DEFAULT NULL,
  `invoice_date_created` date NOT NULL,
  `invoice_time_created` time NOT NULL DEFAULT '00:00:00',
  `invoice_date_modified` datetime NOT NULL,
  `invoice_date_due` date NOT NULL,
  `invoice_number` varchar(100) DEFAULT NULL,
  `invoice_discount_amount` decimal(20,2) DEFAULT NULL,
  `invoice_discount_percent` decimal(20,2) DEFAULT NULL,
  `invoice_terms` longtext NOT NULL,
  `invoice_url_key` char(32) NOT NULL,
  `payment_method` int(11) NOT NULL DEFAULT 0,
  `creditinvoice_parent_id` int(11) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `ip_invoices`
--

INSERT INTO `ip_invoices` (`invoice_id`, `user_id`, `client_id`, `invoice_group_id`, `invoice_status_id`, `is_read_only`, `invoice_password`, `invoice_date_created`, `invoice_time_created`, `invoice_date_modified`, `invoice_date_due`, `invoice_number`, `invoice_discount_amount`, `invoice_discount_percent`, `invoice_terms`, `invoice_url_key`, `payment_method`, `creditinvoice_parent_id`) VALUES
(2, 1, 1, 3, 4, 1, '', '2022-12-14', '00:01:40', '2022-12-14 01:47:02', '2022-12-28', '1', 0.00, 0.00, 'Please pay within 14 days.\nMake payment to:\nAptitude Technology\nAccount: 612983287\nBSB: 013943\nPlease quote the invoice number in the payment reference.', '24NqS9UD7KbJjMrk0dLCPXRYB5fzVG6t', 3, NULL),
(15, 1, 1, 3, 1, NULL, '', '2023-05-03', '10:33:35', '2023-05-03 10:34:26', '2023-05-17', '66', 0.00, 0.00, 'Please pay within 14 days.\nMake payment to:\nChristopher Caston TA Aptitude Technology\n\nAccount: 612983287\nBSB: 013943\nANZ - Airwallex Pty Ltd\nPlease quote the invoice number in the payment reference.', 'gSNlfDcuXoZAVaUMOEezxGtCb45FHhTK', 0, NULL),
(6, 1, 2, 3, 4, 1, '', '2023-01-08', '02:59:33', '2023-01-08 03:39:33', '2023-01-22', '2', 0.00, 0.00, 'Please pay within 14 days.\nMake payment to:\nChristopher Caston TA Aptitude Technology\n\nAccount: 612983287\nBSB: 013943\nANZ - Airwallex Pty Ltd\nPlease quote the invoice number in the payment reference.', 'PchWN30j7bZlJyH1nCQ6UgaYF89wrRfs', 3, NULL),
(16, 1, 5, 3, 2, NULL, '', '2023-05-02', '09:32:29', '2023-05-04 09:34:16', '2023-05-16', '6', 0.00, 0.00, 'Please pay within 14 days.\nMake payment to:\nChristopher Caston TA Aptitude Technology\n\nAccount: 612983287\nBSB: 013943\nANZ - Airwallex Pty Ltd\nPlease quote the invoice number in the payment reference.', 'rJwHqdVMagOo53Sj0zsQmRlB7vDAbY4p', 0, NULL),
(17, 1, 6, 3, 4, 1, '', '2023-05-09', '10:58:24', '2023-05-09 11:01:19', '2023-05-23', '7', 0.00, 0.00, 'Please pay within 14 days.\nMake payment to:\nChristopher Caston TA Aptitude Technology\n\nBANK NAME: ANZ - Airwallex Pty Ltd\nAccount: 612983287\nBSB: 013943\n\nPlease quote the invoice number in the payment reference.', 'mGJZtqX1epsH57w8yrdnga6z3FvCIfUV', 3, NULL),
(10, 1, 3, 3, 4, 1, '', '2023-02-01', '07:22:12', '2023-02-01 07:26:35', '2023-02-15', '3', 0.00, 0.00, 'Please pay within 14 days.\nMake payment to:\nChristopher Caston TA Aptitude Technology\n\nAccount: 612983287\nBSB: 013943\nANZ - Airwallex Pty Ltd\nPlease quote the invoice number in the payment reference.', 'TD97AdbIMJYRzX3cCPor5OQ0HiUSh16y', 0, NULL),
(18, 1, 8, 3, 3, NULL, '', '2023-05-23', '02:52:36', '2023-05-23 02:54:37', '2023-06-06', '8', 0.00, 0.00, 'Please pay within 14 days.\nMake payment to:\nChristopher Caston TA Aptitude Technology\n\nBANK NAME: ANZ - Airwallex Pty Ltd\nAccount: 612983287\nBSB: 013943\n\nPlease quote the invoice number in the payment reference.', 'mgIBK7DriCRtvnPG1S4e0pu5aWFTxJNd', 0, NULL),
(13, 1, 4, 3, 4, 1, '', '2023-04-30', '10:32:20', '2023-04-30 10:37:50', '2023-05-14', '4', 0.00, 0.00, 'Please pay within 14 days.\nMake payment to:\nChristopher Caston TA Aptitude Technology\n\nAccount: 612983287\nBSB: 013943\nANZ - Airwallex Pty Ltd\nPlease quote the invoice number in the payment reference.', 'dW2RyOxtG0fMH3TpQlYmUE9Ag87zhe5s', 3, NULL),
(14, 1, 5, 3, 4, 1, '', '2023-05-02', '10:29:19', '2023-05-04 09:29:49', '2023-05-16', '5', 0.00, 0.00, 'Please pay within 14 days.\nMake payment to:\nChristopher Caston TA Aptitude Technology\n\nAccount: 612983287\nBSB: 013943\nANZ - Airwallex Pty Ltd\nPlease quote the invoice number in the payment reference.', 'YEd1WeLiC9A6oUcPBlQjtn5mK4NOqays', 3, NULL),
(19, 1, 9, 3, 4, 1, '', '2023-05-28', '01:24:46', '2023-05-31 23:12:20', '2023-06-11', '9', 0.00, 0.00, 'Please pay within 14 days.\nMake payment to:\nChristopher Caston TA Aptitude Technology\n\nBANK NAME: ANZ - Airwallex Pty Ltd\nAccount: 612983287\nBSB: 013943\n\nPlease quote the invoice number in the payment reference.', 'CT6Bin38GkE4DyAHbp7heg2X9vumJZ1x', 3, NULL),
(20, 1, 10, 3, 4, 1, '', '2023-06-19', '08:44:34', '2023-06-19 08:55:04', '2023-07-03', '10', 0.00, 0.00, 'Please pay within 14 days.\nMake payment to:\nChristopher Caston TA Aptitude Technology\n\nBANK NAME: ANZ - Airwallex Pty Ltd\nAccount: 612983287\nBSB: 013943\n\nPlease quote the invoice number in the payment reference.', 'RdgbclFiohfZzB24VvJuU368ETeqarw7', 3, NULL),
(21, 1, 10, 3, 4, 1, '', '2023-06-21', '05:12:43', '2023-06-21 05:13:12', '2023-07-05', '11', 0.00, 0.00, 'Please pay within 14 days.\nMake payment to:\nChristopher Caston TA Aptitude Technology\n\nBANK NAME: ANZ - Airwallex Pty Ltd\nAccount: 612983287\nBSB: 013943\n\nPlease quote the invoice number in the payment reference.', '8co9RwQafyknql51WG7AtsCIhdj3zO0g', 3, NULL),
(22, 1, 11, 3, 4, 1, '', '2023-07-26', '03:59:01', '2023-07-28 05:31:07', '2023-08-09', '12', 0.00, 0.00, 'Please pay within 14 days.\nMake payment to:\nChristopher Caston TA Aptitude Technology\n\nBANK NAME: ANZ - Airwallex Pty Ltd\nAccount: 612983287\nBSB: 013943\n\nPlease quote the invoice number in the payment reference.', 'MUxFIX1Lc8hzDlfVBR4reENOni970sKp', 1, NULL),
(30, 1, 19, 3, 4, 1, '', '2023-12-28', '01:14:48', '2023-12-28 01:52:14', '2024-01-11', '19', 0.00, 0.00, 'Please pay within 14 days.\nMake payment to:\nChristopher Caston TA Aptitude Technology\n\nBANK NAME: ANZ - Airwallex Pty Ltd\nAccount: 612983287\nBSB: 013943\n\nPlease quote the invoice number in the payment reference.', 'VM2pbzlI5gG9Zkn6Sq40AtLPDhCxidfN', 3, NULL),
(24, 1, 12, 3, 4, 1, '', '2023-08-04', '02:56:03', '2023-08-04 02:58:11', '2023-08-18', '13', 0.00, 0.00, 'Please pay within 14 days.\nMake payment to:\nChristopher Caston TA Aptitude Technology\n\nBANK NAME: ANZ - Airwallex Pty Ltd\nAccount: 612983287\nBSB: 013943\n\nPlease quote the invoice number in the payment reference.', 'TKIWp5FVSUsEYXka8rNw63xBvyLnmHCd', 1, NULL),
(25, 1, 13, 3, 4, 1, '', '2023-09-14', '09:37:00', '2023-09-14 09:44:00', '2023-09-28', '14', 0.00, 0.00, 'Please pay within 14 days.\nMake payment to:\nChristopher Caston TA Aptitude Technology\n\nBANK NAME: ANZ - Airwallex Pty Ltd\nAccount: 612983287\nBSB: 013943\n\nPlease quote the invoice number in the payment reference.', 'duZ3BvkWacOKzrbIlqwx8hPS1NjiCsy9', 1, NULL),
(26, 1, 14, 3, 4, 1, '', '2023-09-18', '08:50:29', '2023-09-18 08:54:59', '2023-10-02', '15', 0.00, 0.00, 'Please pay within 14 days.\nMake payment to:\nChristopher Caston TA Aptitude Technology\n\nBANK NAME: ANZ - Airwallex Pty Ltd\nAccount: 612983287\nBSB: 013943\n\nPlease quote the invoice number in the payment reference.', '2C8XnpeOBEWMvPoA3gcYk956rbHzuLJS', 3, NULL),
(27, 1, 13, 3, 4, 1, '', '2023-09-25', '01:57:57', '2023-09-25 02:11:41', '2023-10-09', '16', 0.00, 0.00, 'Please pay within 14 days.\nMake payment to:\nChristopher Caston TA Aptitude Technology\n\nBANK NAME: ANZ - Airwallex Pty Ltd\nAccount: 612983287\nBSB: 013943\n\nPlease quote the invoice number in the payment reference.', 'zTh1YAuVRnQFWZXofNcxqerwdka5m6s9', 1, NULL),
(28, 1, 15, 3, 4, 1, '', '2023-10-08', '11:01:37', '2023-10-09 03:19:56', '2023-10-22', '17', 0.00, 0.00, 'Please pay within 14 days.\nMake payment to:\nChristopher Caston TA Aptitude Technology\n\nBANK NAME: ANZ - Airwallex Pty Ltd\nAccount: 612983287\nBSB: 013943\n\nPlease quote the invoice number in the payment reference.', 'P6Xq7eTIS3HJbvn1frELlM590apg8UdF', 3, NULL),
(29, 1, 13, 3, 4, 1, '', '2023-10-10', '04:03:28', '2023-10-10 04:12:07', '2023-10-24', '18', 0.00, 0.00, 'Please pay within 14 days.\nMake payment to:\nChristopher Caston TA Aptitude Technology\n\nBANK NAME: ANZ - Airwallex Pty Ltd\nAccount: 612983287\nBSB: 013943\n\nPlease quote the invoice number in the payment reference.', 'wCD79tmlGukQzXyVAIUW8Ev3c1sjKLiB', 3, NULL),
(31, 1, 20, 3, 4, 1, '', '2023-12-28', '02:17:29', '2023-12-28 06:02:55', '2024-01-11', '20', 0.00, 0.00, 'Please pay within 14 days.\nMake payment to:\nChristopher Caston TA Aptitude Technology\n\nBANK NAME: ANZ - Airwallex Pty Ltd\nAccount: 612983287\nBSB: 013943\n\nPlease quote the invoice number in the payment reference.', 'LMk1bVygwGelAxRzrf6DJuTd9YI5htEa', 3, NULL),
(32, 1, 20, 3, 4, 1, '', '2024-01-05', '11:22:27', '2024-01-06 09:32:35', '2024-01-19', '21', 0.00, 0.00, 'Please pay within 14 days.\nMake payment to:\nChristopher Caston TA Aptitude Technology\n\nBANK NAME: ANZ - Airwallex Pty Ltd\nAccount: 612983287\nBSB: 013943\n\nPlease quote the invoice number in the payment reference.', 'VIQ8NwRHvXnD6oG3ZcFa1sL5YP4ABukp', 3, NULL),
(33, 1, 22, 3, 4, 1, '', '2024-02-15', '05:09:06', '2024-02-15 05:09:41', '2024-02-29', '22', 0.00, 0.00, 'Please pay within 14 days.\nMake payment to:\nChristopher Caston TA Aptitude Technology\n\nBANK NAME: ANZ - Airwallex Pty Ltd\nAccount: 612983287\nBSB: 013943\n\nPlease quote the invoice number in the payment reference.', '0QPsEWhBVLGX79ZpvduY6fSFxAItoJcb', 3, NULL),
(34, 1, 22, 3, 4, 1, '', '2024-02-19', '05:23:23', '2024-02-19 05:28:51', '2024-03-04', '23', 0.00, 0.00, 'Please pay within 14 days.\nMake payment to:\nChristopher Caston TA Aptitude Technology\n\nBANK NAME: ANZ - Airwallex Pty Ltd\nAccount: 612983287\nBSB: 013943\n\nPlease quote the invoice number in the payment reference.', 'xT7NjrwRI8EsKgAyio4hutmCYVdaqOH5', 3, NULL),
(35, 1, 23, 3, 4, 1, '', '2024-02-23', '01:57:34', '2024-02-23 05:25:40', '2024-03-08', '24', 0.00, 0.00, 'Please pay within 14 days.\nMake payment to:\nChristopher Caston TA Aptitude Technology\n\nBANK NAME: ANZ - Airwallex Pty Ltd\nAccount: 612983287\nBSB: 013943\n\nPlease quote the invoice number in the payment reference.', 'oi5pkcRF7AGh6EVT3zC8mUbDSn1e9PJZ', 3, NULL),
(36, 1, 22, 3, 4, 1, '', '2024-02-26', '22:56:13', '2024-02-26 22:57:45', '2024-03-11', '25', 0.00, 0.00, 'Please pay within 14 days.\nMake payment to:\nChristopher Caston TA Aptitude Technology\n\nBANK NAME: ANZ - Airwallex Pty Ltd\nAccount: 612983287\nBSB: 013943\n\nPlease quote the invoice number in the payment reference.', 'AurSfdXJbNk6oH9eTlEhFUR8aqWZPDpz', 3, NULL),
(37, 1, 1, 3, 4, 1, '', '2024-03-03', '02:00:05', '2024-03-03 02:03:08', '2024-03-17', '26', 0.00, 0.00, 'Please pay within 14 days.\nMake payment to:\nChristopher Caston TA Aptitude Technology\n\nBANK NAME: ANZ - Airwallex Pty Ltd\nAccount: 612983287\nBSB: 013943\n\nPlease quote the invoice number in the payment reference.', 'cVWlxJeyzusGDUvhO1LjYIXtai3MCb5q', 0, NULL),
(38, 1, 1, 3, 3, NULL, '', '2024-03-03', '02:36:24', '2024-03-03 02:59:35', '2024-03-17', '27', 0.00, 0.00, 'Please pay within 14 days.\nMake payment to:\nChristopher Caston TA Aptitude Technology\n\nBANK NAME: ANZ - Airwallex Pty Ltd\nAccount: 612983287\nBSB: 013943\n\nPlease quote the invoice number in the payment reference.', 'bu9nBsErhWm8GVzfaRJIOjNSD1Uvc02p', 0, NULL),
(39, 1, 22, 3, 4, 1, '', '2024-03-05', '02:56:53', '2024-03-05 02:57:27', '2024-03-19', '28', 0.00, 0.00, 'Please pay within 14 days.\nMake payment to:\nChristopher Caston TA Aptitude Technology\n\nBANK NAME: ANZ - Airwallex Pty Ltd\nAccount: 612983287\nBSB: 013943\n\nPlease quote the invoice number in the payment reference.', 'W2A78VuZYcXKxJsdUBjqk3rHazDl0eMf', 3, NULL),
(40, 1, 25, 3, 4, 1, '', '2024-03-06', '21:32:03', '2024-03-06 21:33:41', '2024-03-20', '29', 0.00, 0.00, 'Please pay within 14 days.\nMake payment to:\nChristopher Caston TA Aptitude Technology\n\nBANK NAME: ANZ - Airwallex Pty Ltd\nAccount: 612983287\nBSB: 013943\n\nPlease quote the invoice number in the payment reference.', '9ofWQKgez4YJnyxG1RCIaiuB5LqwHTPU', 0, NULL),
(41, 1, 25, 3, 3, NULL, '', '2024-03-06', '21:34:11', '2024-03-06 21:35:15', '2024-03-20', '30', 0.00, 0.00, 'Please pay within 14 days.\nMake payment to:\nChristopher Caston TA Aptitude Technology\n\nBANK NAME: ANZ - Airwallex Pty Ltd\nAccount: 612983287\nBSB: 013943\n\nPlease quote the invoice number in the payment reference.', 'n1IPs8f3xEruHOiLTMvGcQXgAhkWY49o', 0, NULL),
(42, 1, 1, 3, 3, NULL, '', '2024-03-07', '11:57:37', '2024-03-07 12:56:32', '2024-03-21', '31', 0.00, 0.00, 'Please pay within 14 days.\nMake payment to:\nChristopher Caston TA Aptitude Technology\n\nBANK NAME: ANZ - Airwallex Pty Ltd\nAccount: 612983287\nBSB: 013943\n\nPlease quote the invoice number in the payment reference.', 'THPDLZ5eacEmstK8hpV2zJk1uFqQYBG7', 0, NULL),
(43, 1, 7, 3, 4, 1, '', '2024-03-08', '02:49:34', '2024-03-08 02:51:24', '2024-03-22', '32', 0.00, 0.00, 'Please pay within 14 days.\nMake payment to:\nChristopher Caston TA Aptitude Technology\n\nBANK NAME: ANZ - Airwallex Pty Ltd\nAccount: 612983287\nBSB: 013943\n\nPlease quote the invoice number in the payment reference.', 'S1TfUVkMp3Ic0YxjtFHiDasqBLQ4JWEC', 1, NULL),
(44, 1, 24, 3, 4, 1, '', '2024-03-08', '04:42:17', '2024-03-08 06:21:17', '2024-03-22', '33', 0.00, 0.00, 'Please pay within 14 days.\nMake payment to:\nChristopher Caston TA Aptitude Technology\n\nBANK NAME: ANZ - Airwallex Pty Ltd\nAccount: 612983287\nBSB: 013943\n\nPlease quote the invoice number in the payment reference.', '7w4vjhpneglou6Sy8Nxt03YH91AQmF5c', 3, NULL),
(45, 1, 26, 3, 4, 1, '', '2024-03-08', '09:53:11', '2024-03-08 09:53:52', '2024-03-22', '34', 0.00, 0.00, 'Please pay within 14 days.\nMake payment to:\nChristopher Caston TA Aptitude Technology\n\nBANK NAME: ANZ - Airwallex Pty Ltd\nAccount: 612983287\nBSB: 013943\n\nPlease quote the invoice number in the payment reference.', '0dGTK2QE4OZ5syfh7vtM3XnV6gPAejwk', 1, NULL),
(46, 1, 22, 3, 4, 1, '', '2024-03-11', '01:34:23', '2024-03-11 01:51:22', '2024-03-25', '35', 0.00, 0.00, 'Please pay within 14 days.\nMake payment to:\nChristopher Caston TA Aptitude Technology\n\nBANK NAME: ANZ - Airwallex Pty Ltd\nAccount: 612983287\nBSB: 013943\n\nPlease quote the invoice number in the payment reference.', 'z30lyeXOhLqgSK2TCQNUmZrDio6xIkBc', 3, NULL),
(47, 1, 23, 3, 4, 1, '', '2024-03-13', '01:58:15', '2024-03-24 22:21:25', '2024-03-27', '36', 0.00, 0.00, 'Please pay within 14 days.\nMake payment to:\nChristopher Caston TA Aptitude Technology\n\nBANK NAME: ANZ - Airwallex Pty Ltd\nAccount: 612983287\nBSB: 013943\n\nPlease quote the invoice number in the payment reference.', 'L6efVP4U0KwnyDCm2sdvQ1ca73NMYqzx', 3, NULL),
(48, 1, 8, 3, 4, 1, '', '2024-04-10', '10:30:06', '2024-04-10 10:35:11', '2024-04-24', '37', 0.00, 0.00, 'Please pay within 14 days.\nMake payment to:\nChristopher Caston TA Aptitude Technology\n\nBANK NAME: ANZ - Airwallex Pty Ltd\nAccount: 612983287\nBSB: 013943\n\nPlease quote the invoice number in the payment reference.', 'pMSnC7s0H2AUJuZW4yPGmdgqNlFrKOha', 3, NULL),
(49, 1, 8, 3, 4, 1, '', '2024-04-16', '01:34:23', '2024-04-16 01:35:42', '2024-04-30', '38', 0.00, 0.00, 'Please pay within 14 days.\nMake payment to:\nChristopher Caston TA Aptitude Technology\n\nBANK NAME: ANZ - Airwallex Pty Ltd\nAccount: 612983287\nBSB: 013943\n\nPlease quote the invoice number in the payment reference.', 'TmrZyLFptPlM0A9kUb7ExqQ6OIuY5vSK', 3, NULL),
(50, 1, 13, 3, 4, 1, '', '2024-05-02', '06:52:15', '2024-05-05 10:58:15', '2024-05-16', '39', 0.00, 0.00, 'Please pay within 14 days.\nMake payment to:\nChristopher Caston TA Aptitude Technology\n\nBANK NAME: ANZ - Airwallex Pty Ltd\nAccount: 612983287\nBSB: 013943\n\nPlease quote the invoice number in the payment reference.', 'FGhfE9lMgU7kbZNYRizmWpoJAw5qB2HP', 3, NULL),
(51, 1, 28, 3, 4, 1, '', '2024-05-10', '08:43:35', '2024-05-10 11:08:17', '2024-05-24', '40', 0.00, 0.00, 'Please pay within 14 days.\nMake payment to:\nChristopher Caston TA Aptitude Technology\n\nBANK NAME: ANZ - Airwallex Pty Ltd\nAccount: 612983287\nBSB: 013943\n\nPlease quote the invoice number in the payment reference.', 'GuUzr2AnfvoFW7DxPYpHKOCMi0jLm4yd', 3, NULL),
(52, 1, 23, 3, 1, NULL, '', '2024-05-23', '02:00:51', '2024-05-23 02:00:56', '2024-06-06', '78', NULL, NULL, 'Please pay within 14 days.\r\nMake payment to:\r\nChristopher Caston TA Aptitude Technology\r\n\r\nBANK NAME: ANZ - Airwallex Pty Ltd\r\nAccount: 612983287\r\nBSB: 013943\r\n\r\nPlease quote the invoice number in the payment reference.', 'suXTWB4EJrcwMep98Ha2OlFj1mS0v7gU', 0, NULL),
(53, 1, 23, 3, 4, 1, '', '2024-05-23', '02:05:57', '2024-05-23 02:28:03', '2024-06-06', '41', 0.00, 0.00, 'Please pay within 14 days.\nMake payment to:\nChristopher Caston TA Aptitude Technology\n\nBANK NAME: ANZ - Airwallex Pty Ltd\nAccount: 612983287\nBSB: 013943\n\nPlease quote the invoice number in the payment reference.', 'v9DLBypJdaNKmrs1GnWIFuwVUtzb3X8R', 1, NULL),
(54, 1, 30, 3, 4, 1, '', '2024-06-04', '04:27:45', '2024-06-05 02:56:12', '2024-06-18', '42', 0.00, 0.00, 'Please pay within 14 days.\nMake payment to:\nChristopher Caston TA Aptitude Technology\n\nBANK NAME: ANZ - Airwallex Pty Ltd\nAccount: 612983287\nBSB: 013943\n\nPlease quote the invoice number in the payment reference.', 'u6TYqy5wIUpbSCs8FJDax0erVPZidg9k', 3, NULL),
(59, 1, 31, 3, 4, 1, '', '2024-07-10', '08:02:57', '2024-07-10 08:04:46', '2024-07-24', '46', 0.00, 0.00, 'Please pay within 14 days.\nMake payment to:\nChristopher Caston \n\nBANK NAME: ANZ - Airwallex Pty Ltd\nAccount: 612983287\nBSB: 013943\n\nPlease quote the invoice number in the payment reference.', 'rhCXm3xD29bkuROB0LsIq6oiVW1HAM4l', 3, NULL),
(56, 1, 33, 3, 4, 1, '', '2024-06-17', '03:11:32', '2024-06-17 03:15:32', '2024-07-01', '43', 0.00, 0.00, 'Please pay within 14 days.\nMake payment to:\nChristopher Caston TA Aptitude Technology\n\nBANK NAME: ANZ - Airwallex Pty Ltd\nAccount: 612983287\nBSB: 013943\n\nPlease quote the invoice number in the payment reference.', 'A3yl2zZ0NvYaDTWUbhR8Lo4HpKu5qMit', 3, NULL),
(57, 1, 34, 3, 4, 1, '', '2024-06-18', '03:59:23', '2024-06-18 04:02:36', '2024-07-02', '44', 0.00, 0.00, 'Please pay within 14 days.\nMake payment to:\nChristopher Caston TA Aptitude Technology\n\nBANK NAME: ANZ - Airwallex Pty Ltd\nAccount: 612983287\nBSB: 013943\n\nPlease quote the invoice number in the payment reference.', 'PW423iljIN0koy5KX8eqZwTgsbRzAtLh', 1, NULL),
(58, 1, 22, 3, 4, 1, '', '2024-06-20', '01:21:23', '2024-06-20 01:24:44', '2024-07-04', '45', 0.00, 0.00, 'Please pay within 14 days.\nMake payment to:\nChristopher Caston \n\nBANK NAME: ANZ - Airwallex Pty Ltd\nAccount: 612983287\nBSB: 013943\n\nPlease quote the invoice number in the payment reference.', 'ygD4I7UiEp8xn1Y0TFP9bXKzjSZBqtcm', 3, NULL),
(60, 1, 13, 3, 4, 1, '', '2024-07-22', '05:14:24', '2024-07-23 07:02:42', '2024-08-05', '47', 0.00, 0.00, 'Please pay within 14 days.\nMake payment to:\nChristopher Caston \n\nBANK NAME: ANZ - Airwallex Pty Ltd\nAccount: 612983287\nBSB: 013943\n\nPlease quote the invoice number in the payment reference.', 'pBIKDs15uMH3d7xhFzGeN0qyilVQCwnL', 3, NULL),
(61, 1, 13, 3, 4, 1, '', '2024-07-29', '07:43:05', '2024-07-29 07:53:43', '2024-08-12', '48', 0.00, 0.00, 'Please pay within 14 days.\nMake payment to:\nChristopher Caston \n\nBANK NAME: ANZ - Airwallex Pty Ltd\nAccount: 612983287\nBSB: 013943\n\nPlease quote the invoice number in the payment reference.', 'hiLE3TrHV140uajwxkYWeoKGDvtfpCNQ', 3, NULL),
(62, 1, 36, 3, 4, 1, '', '2024-08-13', '07:41:18', '2024-08-15 01:39:29', '2024-08-27', '49', 0.00, 0.00, 'Please pay within 14 days.\nMake payment to:\nChristopher Caston \n\nBANK NAME: ANZ - Airwallex Pty Ltd\nAccount: 612983287\nBSB: 013943\n\nPlease quote the invoice number in the payment reference.', '8KYGeQ6kb3cxh2IB7maJondwVHijlsTt', 3, NULL),
(63, 1, 13, 3, 4, 1, '', '2024-08-15', '04:49:24', '2024-08-16 02:21:38', '2024-08-29', '50', 0.00, 0.00, 'Please pay within 14 days.\nMake payment to:\nChristopher Caston \n\nBANK NAME: ANZ - Airwallex Pty Ltd\nAccount: 612983287\nBSB: 013943\n\nPlease quote the invoice number in the payment reference.', 'S56K9yeZhdRowx1Wj7iTcvJHl2nEDY0z', 3, NULL),
(64, 1, 1, 3, 1, NULL, '', '2024-08-28', '03:49:24', '2024-08-28 03:50:02', '2024-09-11', '67', 0.00, 0.00, 'Please pay within 14 days.\nMake payment to:\nChristopher Caston \n\nBANK NAME: ANZ - Airwallex Pty Ltd\nAccount: 612983287\nBSB: 013943\n\nPlease quote the invoice number in the payment reference.', 'Im9uO8HMBZVEA4LtW3RgiawvNkCKh0fF', 0, NULL),
(65, 1, 6, 3, 4, 1, '', '2024-09-12', '05:45:57', '2024-09-12 05:49:19', '2024-09-26', '51', 0.00, 0.00, 'Please pay within 14 days.\nMake payment to:\nChristopher Caston \n\nBANK NAME: ANZ - Airwallex Pty Ltd\nAccount: 612983287\nBSB: 013943\n\nPlease quote the invoice number in the payment reference.', 'rtapJmXljdvMPq8OnxAeSy1fk6cI5CzE', 3, NULL),
(66, 1, 38, 3, 4, 1, '', '2024-09-13', '06:24:42', '2024-09-13 06:28:37', '2024-09-27', '68', 0.00, 0.00, 'Please pay within 14 days.\nMake payment to:\nChristopher Caston \n\nBANK NAME: ANZ - Airwallex Pty Ltd\nAccount: 612983287\nBSB: 013943\n\nPlease quote the invoice number in the payment reference.', 'BAMOPaqnX8s9LKkGicxHVoyjJ0pDW2Rm', 1, NULL),
(67, 1, 38, 3, 4, 1, '', '2024-09-14', '01:16:21', '2024-09-14 01:16:36', '2024-09-28', '52', 0.00, 0.00, 'Please pay within 14 days.\nMake payment to:\nChristopher Caston \n\nBANK NAME: ANZ - Airwallex Pty Ltd\nAccount: 612983287\nBSB: 013943\n\nPlease quote the invoice number in the payment reference.', 'ipzDkb3tL6XrM7NIxZVS50CaAhYy2Bj1', 1, NULL),
(68, 1, 38, 3, 4, 1, '', '2024-09-19', '02:12:49', '2024-09-19 02:14:14', '2024-10-03', '53', 0.00, 0.00, 'Please pay within 14 days.\nMake payment to:\nChristopher Caston \n\nBANK NAME: ANZ - Airwallex Pty Ltd\nAccount: 612983287\nBSB: 013943\n\nPlease quote the invoice number in the payment reference.', 'juFRl50hEyaKonkwqdAtZcsMONUr4f7x', 1, NULL),
(69, 1, 39, 3, 4, 1, '', '2024-09-30', '08:47:44', '2024-09-30 08:51:28', '2024-10-14', '54', 0.00, 0.00, 'Please pay within 14 days.\nMake payment to:\nChristopher Caston \n\nBANK NAME: ANZ - Airwallex Pty Ltd\nAccount: 612983287\nBSB: 013943\n\nPlease quote the invoice number in the payment reference.', 'bZImcvRfhugzSetQYGk65UV7Wi2Jd98A', 1, NULL),
(70, 1, 40, 3, 4, 1, '', '2024-11-08', '09:30:23', '2024-11-08 09:34:17', '2024-11-22', '69', 0.00, 0.00, 'Please pay within 14 days.\nMake payment to:\nChristopher Caston \n\nBANK NAME: ANZ - Airwallex Pty Ltd\nAccount: 612983287\nBSB: 013943\n\nPlease quote the invoice number in the payment reference.', '2ckVSZjzO05EAHesTxR8KXlYMro4FvDI', 1, NULL),
(71, 1, 8, 3, 3, NULL, '', '2024-11-11', '04:06:30', '2024-11-11 04:08:49', '2024-11-25', '55', 0.00, 0.00, 'Please pay within 14 days.\nMake payment to:\nChristopher Caston \n\nBANK NAME: ANZ - Airwallex Pty Ltd\nAccount: 612983287\nBSB: 013943\n\nPlease quote the invoice number in the payment reference.', 'Y1mqhOFlkvEGarnQSMd5JxiKC3NybcIw', 0, NULL),
(72, 1, 7, 3, 4, 1, '', '2024-12-13', '03:43:44', '2024-12-13 03:44:47', '2024-12-27', '56', 0.00, 0.00, 'Please pay within 14 days.\nMake payment to:\nChristopher Caston \n\nBANK NAME: ANZ - Airwallex Pty Ltd\nAccount: 612983287\nBSB: 013943\n\nPlease quote the invoice number in the payment reference.', 'euOqNJRngcW6Ftvi1lQkw3jHKBSX57ME', 1, NULL),
(73, 1, 22, 3, 4, 1, '', '2025-01-20', '23:36:01', '2025-01-21 23:30:18', '2025-02-03', '57', 0.00, 0.00, 'Please pay within 14 days.\nMake payment to:\nTYPE1CIV Pty Ltd\n\nBANK NAME: ANZ - Airwallex Pty Ltd\nAccount: 612082265\nBSB: 013943\n\nPlease quote the invoice number in the payment reference.', 'Xep8ZgNsbOUcjhBdLPv6QVKYHDfxzrit', 3, NULL),
(74, 1, 13, 3, 1, NULL, '', '2025-01-28', '03:16:35', '2025-01-29 13:07:31', '2025-02-11', '70', 0.00, 0.00, 'Please pay within 14 days.\nMake payment to:\nTYPE1CIV Pty Ltd\n\nBANK NAME: ANZ - Airwallex Pty Ltd\nAccount: 612082265\nBSB: 013943\n\nPlease quote the invoice number in the payment reference.', 'skBabE071J5oWFzRlUvYPIg6HTQXhpum', 0, NULL),
(75, 1, 28, 3, 4, 1, '', '2025-02-11', '01:22:59', '2025-02-12 04:45:27', '2025-02-25', '58', 0.00, 0.00, 'Please pay within 14 days.\nMake payment to:\nTYPE1CIV Pty Ltd\n\nBANK NAME: ANZ - Airwallex Pty Ltd\nAccount: 612082265\nBSB: 013943\n\nPlease quote the invoice number in the payment reference.', '5SsqRdBle4TzoW28Nh6fUPOrmMyK3pHJ', 3, NULL),
(76, 1, 11, 3, 2, NULL, '', '2025-02-22', '03:17:55', '2025-02-22 03:20:06', '2025-03-08', '59', 0.00, 0.00, 'Please pay within 14 days.\nMake payment to:\nTYPE1CIV Pty Ltd\n\nBANK NAME: ANZ - Airwallex Pty Ltd\nAccount: 612082265\nBSB: 013943\n\nPlease quote the invoice number in the payment reference.', 'YJPKuxt0296XFfHqQo13TvkcDBzEjbZN', 0, NULL),
(77, 1, 43, 3, 4, 1, '', '2025-03-04', '03:48:13', '2025-03-04 03:49:21', '2025-03-18', '60', 0.00, 0.00, 'Please pay within 14 days.\nMake payment to:\nTYPE1CIV Pty Ltd\n\nBANK NAME: ANZ - Airwallex Pty Ltd\nAccount: 612082265\nBSB: 013943\n\nPlease quote the invoice number in the payment reference.', 'xtnHNoPWwDX0qzaMFlK6rh9YAmVBEO3d', 3, NULL),
(78, 1, 38, 3, 1, NULL, '', '2025-05-03', '11:16:37', '2025-05-03 11:16:44', '2025-05-17', '71', NULL, NULL, 'Please pay within 14 days.\r\nMake payment to:\r\nTYPE1CIV Pty Ltd\r\n\r\nBANK NAME: ANZ - Airwallex Pty Ltd\r\nAccount: 612082265\r\nBSB: 013943\r\n\r\nPlease quote the invoice number in the payment reference.', 'xRTiaF437goJkC6jKyZBwce59X0dOmLp', 0, NULL),
(79, 1, 38, 3, 4, 1, '', '2025-05-03', '11:19:21', '2025-05-05 01:09:40', '2025-05-17', '61', 0.00, 0.00, 'Please pay within 14 days.\nMake payment to:\nTYPE1CIV Pty Ltd\n\nBANK NAME: ANZ - Airwallex Pty Ltd\nAccount: 612082265\nBSB: 013943\n\nPlease quote the invoice number in the payment reference.', 'Gs2F3ozxKuURlTt9p8SeJr5Bj7dPAihL', 1, NULL),
(80, 1, 44, 3, 4, 1, '', '2025-05-27', '07:10:19', '2025-06-15 09:00:27', '2025-06-10', '62', 0.00, 0.00, 'Please pay within 14 days.\nMake payment to:\nTYPE1CIV Pty Ltd\n\nBANK NAME: ANZ - Airwallex Pty Ltd\nAccount: 612082265\nBSB: 013943\n\nPlease quote the invoice number in the payment reference.', 'dF2PZIefYxkurmvgol4i5VMybn86Dh1z', 3, NULL),
(81, 1, 18, 3, 2, NULL, '', '2025-06-16', '02:41:35', '2025-06-16 02:46:03', '2025-06-30', '63', 0.00, 0.00, 'Please pay within 14 days.\nMake payment to:\nTYPE1CIV Pty Ltd\n\nBANK NAME: ANZ - Airwallex Pty Ltd\nAccount: 612082265\nBSB: 013943\n\nPlease quote the invoice number in the payment reference.', 'u17hdLiVl3aJGseWjT4Zy9nSRvHDYpzr', 0, NULL),
(82, 1, 8, 3, 2, NULL, '', '2025-06-24', '04:58:22', '2025-06-24 05:04:33', '2025-07-08', '64', 0.00, 0.00, 'Please pay within 14 days.\nMake payment to:\nTYPE1CIV Pty Ltd\n\nBANK NAME: ANZ - Airwallex Pty Ltd\nAccount: 612082265\nBSB: 013943\n\nPlease quote the invoice number in the payment reference.', '64mvsqC2fBOM0KDoQAyEZndSG1HhcTJi', 0, NULL),
(83, 1, 25, 3, 1, NULL, '', '2025-07-08', '00:00:03', '2025-07-08 00:00:18', '2025-07-22', '72', NULL, NULL, 'Please pay within 14 days.\r\nMake payment to:\r\nTYPE1CIV Pty Ltd\r\n\r\nBANK NAME: ANZ - Airwallex Pty Ltd\r\nAccount: 612082265\r\nBSB: 013943\r\n\r\nPlease quote the invoice number in the payment reference.', 'TQ8jlOf2gqP95thkGLBUybMWECa1nSuH', 0, NULL),
(84, 1, 25, 3, 1, NULL, '', '2025-07-08', '08:01:40', '2025-07-08 08:01:59', '2025-07-22', '73', NULL, NULL, 'Please pay within 14 days.\r\nMake payment to:\r\nTYPE1CIV Pty Ltd\r\n\r\nBANK NAME: ANZ - Airwallex Pty Ltd\r\nAccount: 612082265\r\nBSB: 013943\r\n\r\nPlease quote the invoice number in the payment reference.', 'wUTPgdm2fMu3i1A6o9RSGNYWa8bOXryE', 0, NULL),
(85, 1, 25, 3, 1, NULL, '', '2025-07-08', '08:06:02', '2025-07-08 08:06:44', '2025-07-22', '74', NULL, NULL, 'Please pay within 14 days.\r\nMake payment to:\r\nTYPE1CIV Pty Ltd\r\n\r\nBANK NAME: ANZ - Airwallex Pty Ltd\r\nAccount: 612082265\r\nBSB: 013943\r\n\r\nPlease quote the invoice number in the payment reference.', 'GIfaNB2g7ZJWL8oTp5xMOh3rF60zYijl', 0, NULL),
(86, 1, 25, 3, 1, NULL, '', '2025-07-08', '08:15:05', '2025-07-08 08:15:12', '2025-07-22', '75', NULL, NULL, 'Please pay within 14 days.\r\nMake payment to:\r\nTYPE1CIV Pty Ltd\r\n\r\nBANK NAME: ANZ - Airwallex Pty Ltd\r\nAccount: 612082265\r\nBSB: 013943\r\n\r\nPlease quote the invoice number in the payment reference.', '7M6SwVuFBdteKig4Dpso2PWvAaQHJr5b', 0, NULL),
(87, 1, 25, 3, 1, NULL, '', '2025-07-08', '09:19:27', '2025-07-08 09:19:38', '2025-07-22', '76', NULL, NULL, 'Please pay within 14 days.\r\nMake payment to:\r\nTYPE1CIV Pty Ltd\r\n\r\nBANK NAME: ANZ - Airwallex Pty Ltd\r\nAccount: 612082265\r\nBSB: 013943\r\n\r\nPlease quote the invoice number in the payment reference.', 'vNkiFf52buzU67doBnpxg1EWXaJYm0l4', 0, NULL),
(88, 1, 25, 3, 1, NULL, '', '2025-07-09', '04:05:32', '2025-07-09 04:05:43', '2025-07-23', '77', NULL, NULL, 'Please pay within 14 days.\r\nMake payment to:\r\nTYPE1CIV Pty Ltd\r\n\r\nBANK NAME: ANZ - Airwallex Pty Ltd\r\nAccount: 612082265\r\nBSB: 013943\r\n\r\nPlease quote the invoice number in the payment reference.', 'xXmZhHkBgQ3ylqMiR9UnKGrWfOCAu07J', 0, NULL),
(89, 1, 43, 3, 3, NULL, '', '2025-10-04', '07:21:01', '2025-10-04 07:56:07', '2025-10-18', '65', 0.00, 0.00, 'Please pay within 14 days.\nMake payment to:\nTYPE1CIV Pty Ltd\n\nBANK NAME: ANZ - Airwallex Pty Ltd\nAccount: 612082265\nBSB: 013943\n\nPlease quote the invoice number in the payment reference.', 'Nuem1J6sfrGd4Vlpw89IOTQCkR5iWxEL', 0, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `ip_invoices_recurring`
--

CREATE TABLE `ip_invoices_recurring` (
  `invoice_recurring_id` int(11) NOT NULL,
  `invoice_id` int(11) NOT NULL,
  `recur_start_date` date NOT NULL,
  `recur_end_date` date DEFAULT NULL,
  `recur_frequency` varchar(255) NOT NULL,
  `recur_next_date` date DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `ip_invoice_amounts`
--

CREATE TABLE `ip_invoice_amounts` (
  `invoice_amount_id` int(11) NOT NULL,
  `invoice_id` int(11) NOT NULL,
  `invoice_sign` enum('1','-1') NOT NULL DEFAULT '1',
  `invoice_item_subtotal` decimal(20,2) DEFAULT NULL,
  `invoice_item_tax_total` decimal(20,2) DEFAULT NULL,
  `invoice_tax_total` decimal(20,2) DEFAULT NULL,
  `invoice_total` decimal(20,2) DEFAULT NULL,
  `invoice_paid` decimal(20,2) DEFAULT NULL,
  `invoice_balance` decimal(20,2) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `ip_invoice_amounts`
--

INSERT INTO `ip_invoice_amounts` (`invoice_amount_id`, `invoice_id`, `invoice_sign`, `invoice_item_subtotal`, `invoice_item_tax_total`, `invoice_tax_total`, `invoice_total`, `invoice_paid`, `invoice_balance`) VALUES
(2, 2, '1', 45.00, 0.00, 0.00, 45.00, 45.00, 0.00),
(15, 15, '1', 100.00, 10.00, 0.00, 110.00, 0.00, 110.00),
(6, 6, '1', 25.00, 0.00, 0.00, 25.00, 25.00, 0.00),
(16, 16, '1', 67.00, 6.70, 0.00, 73.70, 0.00, 73.70),
(17, 17, '1', 233.90, 23.39, 0.00, 257.29, 257.29, 0.00),
(10, 10, '1', 100.00, 10.00, 0.00, 110.00, 0.00, 110.00),
(18, 18, '1', 50.00, 5.00, 0.00, 55.00, 0.00, 55.00),
(13, 13, '1', 200.00, 20.00, 0.00, 220.00, 220.00, 0.00),
(14, 14, '1', 310.00, 31.00, 0.00, 341.00, 341.00, 0.00),
(19, 19, '1', 110.00, 11.00, 0.00, 121.00, 121.00, 0.00),
(20, 20, '1', 75.00, 7.50, 0.00, 82.50, 82.50, 0.00),
(21, 21, '1', 167.00, 16.70, 0.00, 183.70, 183.70, 0.00),
(22, 22, '1', 65.00, 6.50, 0.00, 71.50, 71.50, 0.00),
(30, 30, '1', 60.00, 6.00, 0.00, 66.00, 66.00, 0.00),
(24, 24, '1', 50.00, 5.00, 0.00, 55.00, 55.00, 0.00),
(25, 25, '1', 365.00, 20.00, 0.00, 385.00, 385.00, 0.00),
(26, 26, '1', 206.00, 20.60, 0.00, 226.60, 226.60, 0.00),
(27, 27, '1', 348.50, 36.50, 0.00, 385.00, 385.00, 0.00),
(28, 28, '1', 192.00, 19.20, 0.00, 211.20, 211.20, 0.00),
(29, 29, '1', 100.00, 10.00, 0.00, 110.00, 110.00, 0.00),
(31, 31, '1', 330.00, 33.00, 0.00, 363.00, 363.00, 0.00),
(32, 32, '1', 118.00, 11.80, 0.00, 129.80, 129.80, 0.00),
(33, 33, '1', 5984.80, 598.48, 0.00, 6583.28, 6583.28, 0.00),
(34, 34, '1', 400.00, 40.00, 0.00, 440.00, 440.00, 0.00),
(35, 35, '1', 50.00, 5.00, 0.00, 55.00, 55.00, 0.00),
(36, 36, '1', 190.00, 19.00, 0.00, 209.00, 209.00, 0.00),
(37, 37, '1', 10.00, 0.00, 0.00, 10.00, 0.00, 10.00),
(38, 38, '1', 0.00, NULL, 0.00, 0.00, 0.00, 0.00),
(39, 39, '1', 462.82, 46.28, 0.00, 509.10, 509.10, 0.00),
(40, 40, '1', 170.00, 17.00, 0.00, 187.00, 0.00, 187.00),
(41, 41, '1', 170.00, 17.00, 0.00, 187.00, 0.00, 187.00),
(42, 42, '1', 10.00, 1.00, 0.00, 11.00, 0.00, 11.00),
(43, 43, '1', 50.00, 5.00, 0.00, 55.00, 55.00, 0.00),
(44, 44, '1', 204.00, 20.40, 0.00, 224.40, 224.40, 0.00),
(45, 45, '1', 50.00, 5.00, 0.00, 55.00, 55.00, 0.00),
(46, 46, '1', 400.00, 40.00, 0.00, 440.00, 440.00, 0.00),
(47, 47, '1', 50.00, 5.00, 0.00, 55.00, 55.00, 0.00),
(48, 48, '1', 50.00, 5.00, 0.00, 55.00, 55.00, 0.00),
(49, 49, '1', 159.00, 15.90, 0.00, 174.90, 174.90, 0.00),
(50, 50, '1', 268.00, 26.80, 0.00, 294.80, 294.80, 0.00),
(51, 51, '1', 100.00, 10.00, 0.00, 110.00, 110.00, 0.00),
(52, 52, '1', NULL, NULL, NULL, NULL, NULL, NULL),
(53, 53, '1', 80.00, 8.00, 0.00, 88.00, 88.00, 0.00),
(54, 54, '1', 100.00, 10.00, 0.00, 110.00, 110.00, 0.00),
(59, 59, '1', 150.00, 15.00, 0.00, 165.00, 165.00, 0.00),
(56, 56, '1', 30.00, 3.00, 0.00, 33.00, 33.00, 0.00),
(57, 57, '1', 110.00, 11.00, 0.00, 121.00, 121.00, 0.00),
(58, 58, '1', 100.00, 10.00, 0.00, 110.00, 110.00, 0.00),
(60, 60, '1', 400.00, 40.00, 0.00, 440.00, 440.00, 0.00),
(61, 61, '1', 505.00, 50.50, 0.00, 555.50, 555.50, 0.00),
(62, 62, '1', 60.00, 6.00, 0.00, 66.00, 0.00, 66.00),
(63, 63, '1', 545.45, 54.55, 0.00, 600.00, 600.00, 0.00),
(64, 64, '1', 220.00, 22.00, 0.00, 242.00, 0.00, 242.00),
(65, 65, '1', 100.00, 10.00, 0.00, 110.00, 110.00, 0.00),
(66, 66, '1', 400.00, 40.00, 0.00, 440.00, 440.00, 0.00),
(67, 67, '1', 400.00, 40.00, 0.00, 440.00, 440.00, 0.00),
(68, 68, '1', 100.00, 10.00, 0.00, 110.00, 110.00, 0.00),
(69, 69, '1', 197.27, 19.73, 0.00, 217.00, 217.00, 0.00),
(70, 70, '1', 205.00, 0.00, 0.00, 205.00, 205.00, 0.00),
(71, 71, '1', 100.00, 0.00, 0.00, 100.00, 0.00, 100.00),
(72, 72, '1', 50.00, 0.00, 0.00, 50.00, 50.00, 0.00),
(73, 73, '1', 25.00, 2.50, 0.00, 27.50, 27.50, 0.00),
(74, 74, '1', 300.00, 30.00, 0.00, 330.00, 0.00, 330.00),
(75, 75, '1', 100.00, 10.00, 0.00, 110.00, 110.00, 0.00),
(76, 76, '1', 300.00, 30.00, 0.00, 330.00, 200.00, 130.00),
(77, 77, '1', 100.00, 10.00, 0.00, 110.00, 110.00, 0.00),
(78, 78, '1', NULL, NULL, NULL, NULL, NULL, NULL),
(79, 79, '1', 526.00, 52.60, 0.00, 578.60, 578.60, 0.00),
(80, 80, '1', 200.00, 20.00, 0.00, 220.00, 220.00, 0.00),
(81, 81, '1', 90.00, 9.00, 0.00, 99.00, 0.00, 99.00),
(82, 82, '1', 100.00, 10.00, 0.00, 110.00, 0.00, 110.00),
(83, 83, '1', NULL, NULL, NULL, NULL, NULL, NULL),
(84, 84, '1', NULL, NULL, NULL, NULL, NULL, NULL),
(85, 85, '1', NULL, NULL, NULL, NULL, NULL, NULL),
(86, 86, '1', NULL, NULL, NULL, NULL, NULL, NULL),
(87, 87, '1', NULL, NULL, NULL, NULL, NULL, NULL),
(88, 88, '1', NULL, NULL, NULL, NULL, NULL, NULL),
(89, 89, '1', 500.00, 50.00, 0.00, 550.00, 0.00, 550.00);

-- --------------------------------------------------------

--
-- Table structure for table `ip_invoice_custom`
--

CREATE TABLE `ip_invoice_custom` (
  `invoice_custom_id` int(11) NOT NULL,
  `invoice_id` int(11) NOT NULL,
  `invoice_custom_fieldid` int(11) NOT NULL,
  `invoice_custom_fieldvalue` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `ip_invoice_groups`
--

CREATE TABLE `ip_invoice_groups` (
  `invoice_group_id` int(11) NOT NULL,
  `invoice_group_name` text DEFAULT NULL,
  `invoice_group_identifier_format` varchar(255) NOT NULL,
  `invoice_group_next_id` int(11) NOT NULL,
  `invoice_group_left_pad` int(2) NOT NULL DEFAULT 0
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `ip_invoice_groups`
--

INSERT INTO `ip_invoice_groups` (`invoice_group_id`, `invoice_group_name`, `invoice_group_identifier_format`, `invoice_group_next_id`, `invoice_group_left_pad`) VALUES
(3, 'Invoice Default', '{{{id}}}', 66, 0),
(4, 'Quote Default', 'QUO{{{id}}}', 15, 0);

-- --------------------------------------------------------

--
-- Table structure for table `ip_invoice_items`
--

CREATE TABLE `ip_invoice_items` (
  `item_id` int(11) NOT NULL,
  `invoice_id` int(11) NOT NULL,
  `item_tax_rate_id` int(11) NOT NULL DEFAULT 0,
  `item_product_id` int(11) DEFAULT NULL,
  `item_date_added` date NOT NULL,
  `item_task_id` int(11) DEFAULT NULL,
  `item_name` text DEFAULT NULL,
  `item_description` longtext DEFAULT NULL,
  `item_quantity` decimal(10,2) NOT NULL,
  `item_price` decimal(20,2) DEFAULT NULL,
  `item_discount_amount` decimal(20,2) DEFAULT NULL,
  `item_order` int(2) NOT NULL DEFAULT 0,
  `item_is_recurring` tinyint(1) DEFAULT NULL,
  `item_product_unit` varchar(50) DEFAULT NULL,
  `item_product_unit_id` int(11) DEFAULT NULL,
  `item_date` date DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `ip_invoice_items`
--

INSERT INTO `ip_invoice_items` (`item_id`, `invoice_id`, `item_tax_rate_id`, `item_product_id`, `item_date_added`, `item_task_id`, `item_name`, `item_description`, `item_quantity`, `item_price`, `item_discount_amount`, `item_order`, `item_is_recurring`, `item_product_unit`, `item_product_unit_id`, `item_date`) VALUES
(1, 2, 0, 2, '2022-12-14', NULL, 'Orico 2.5 Inch Hard Drive Adapter', 'Turns your 2.5 inch SATA HDD / SSD into 3.5 inch so you can install it into your desktop PC', 1.00, 20.00, NULL, 1, NULL, NULL, NULL, NULL),
(2, 2, 0, 1, '2022-12-14', NULL, 'PC service', '', 0.25, 100.00, NULL, 2, NULL, NULL, NULL, NULL),
(7, 6, 0, 1, '2023-01-08', NULL, 'PC service', 'Troubleshoot and setup modem and wireless router.\nTest internet connection the VoIP', 0.25, 100.00, NULL, 1, NULL, NULL, NULL, NULL),
(8, 10, 2, NULL, '2023-02-01', NULL, 'hour support', 'consult on wireless dongle\nupdate bios\ninstall google chrome\ninstall antivirus', 1.00, 100.00, NULL, 1, NULL, NULL, NULL, NULL),
(9, 13, 2, 1, '2023-04-30', NULL, 'PC service', 'run diagnostics on HP Pavilion desktop\ncreate backup image\ninstall HP recovery image\nrecover files from backup image\n', 2.00, 100.00, NULL, 1, NULL, NULL, NULL, NULL),
(10, 14, 2, 3, '2023-05-02', NULL, 'hours contract rate', 'Work completed for Phil & Jane King.\nInstall SSD and m2. NVME drive in HP laptop\nreinstall Windows\nrecover data\nsetup Office software\nsetup printer\nmisc configurations', 4.00, 60.00, NULL, 1, NULL, NULL, NULL, NULL),
(11, 14, 2, 4, '2023-05-02', NULL, 'Kingston 1TB NV2 2280 NVMe SSD', '', 1.00, 70.00, NULL, 2, NULL, NULL, NULL, NULL),
(14, 16, 2, 5, '2023-05-04', NULL, 'Silicon Power Ace A55 1TB TLC 3D NAND 2.5in SATA III SSD', 'Tentative invoice to cover 2.5\" SSD that is in clients machine and was installed in the available 2.5\" SATA slot.\nWe are at a fork in the road (so to speak) and this can either be removed or used as a local backup drive.', 1.00, 67.00, NULL, 1, NULL, NULL, NULL, NULL),
(13, 15, 2, 1, '2023-05-03', NULL, 'PC service', '', 1.00, 100.00, NULL, 1, NULL, NULL, NULL, NULL),
(15, 17, 2, 6, '2023-05-09', NULL, 'Crucial MX500 2TB 3D NAND SATA 6Gbps 2.5in SSD 560MB/s 510MB/s', 'New faster and higher capacity storage device to replace slow and smaller capacity C drive.', 1.00, 179.00, NULL, 1, NULL, NULL, NULL, NULL),
(16, 17, 2, 7, '2023-05-09', NULL, 'Corsair 8GB (1x8GB) CMSO8GX3M1C1600C11 1600MHz Value Select DDR3L SODIMM RAM', 'Additional RAM chip to increase the available system memory.', 1.00, 54.90, NULL, 2, NULL, NULL, NULL, NULL),
(17, 18, 2, 1, '2023-05-23', NULL, 'PC service', '', 0.50, 100.00, NULL, 1, NULL, NULL, NULL, NULL),
(18, 19, 2, 8, '2023-05-28', NULL, 'Microsoft 365 Family 2021 English APAC 1 Year Subscription Medialess for PC & Mac', '', 1.00, 110.00, NULL, 1, NULL, NULL, NULL, NULL),
(19, 20, 2, 9, '2023-06-19', NULL, 'hours service home', 'installed EMclient for e-mail\ninstall Malware bytes and scanner computer\nuninstalled old programs\ninstalled foxit pdf\nconsulted on upgrade path', 1.50, 50.00, NULL, 1, NULL, NULL, NULL, NULL),
(20, 21, 2, 5, '2023-06-21', NULL, 'Silicon Power Ace A55 1TB TLC 3D NAND 2.5in SATA III SSD', 'New SSD drive to increase the speed and storage capacity of your Toshiba laptop.', 1.00, 67.00, NULL, 1, NULL, NULL, NULL, NULL),
(21, 21, 2, 9, '2023-06-21', NULL, 'hours service home', 'open up Toshiba Satellite Pro L50-A case and remove HDD.\nClone HDD to SSD drive.\nInstall new SSD drive and close Toshiba case. ', 2.00, 50.00, NULL, 2, NULL, NULL, NULL, NULL),
(22, 22, 2, 10, '2023-07-26', NULL, 'Vision Australia Keyboard', '', 1.00, 15.00, NULL, 1, NULL, NULL, NULL, NULL),
(23, 22, 2, 9, '2023-07-26', NULL, 'hours service home', 'install openshell\ninstall malware byes\nconsult on usability ', 1.00, 50.00, NULL, 2, NULL, NULL, NULL, NULL),
(42, 30, 2, 14, '2023-12-28', NULL, 'dvi to display port cable', 'change display port cable on monitor.\nDelete contents of \"socials\" in gmail.', 1.00, 10.00, NULL, 1, NULL, NULL, NULL, NULL),
(43, 30, 2, 9, '2023-12-28', NULL, 'hours service home', '', 1.00, 50.00, NULL, 2, NULL, NULL, NULL, NULL),
(25, 24, 2, 9, '2023-08-04', NULL, 'hours service home', 'recover Windows 10\nsetup MS account\ninstall printers\nsetup software\nimport bookmarks', 1.00, 50.00, NULL, 1, NULL, NULL, NULL, NULL),
(27, 25, 0, 11, '2023-09-14', NULL, 'Crucial BX500 2TB 3D NAND SATA 2.5in SSD', '', 1.00, 145.00, NULL, 1, NULL, NULL, NULL, NULL),
(28, 25, 0, 2, '2023-09-14', NULL, 'Orico 2.5 Inch Hard Drive Adapter', 'Turns your 2.5 inch SATA HDD / SSD into 3.5 inch so you can install it into your desktop PC', 1.00, 20.00, NULL, 2, NULL, NULL, NULL, NULL),
(29, 25, 2, 1, '2023-09-14', NULL, 'PC service', '', 2.00, 100.00, NULL, 3, NULL, NULL, NULL, NULL),
(30, 26, 0, NULL, '2023-09-18', NULL, 'power', '', 1.00, 0.00, NULL, 1, NULL, NULL, NULL, NULL),
(31, 26, 2, 12, '2023-09-18', NULL, 'Corsair 550W CX550F RGB White 80+ Bronze Power Supply', '', 1.00, 106.00, NULL, 2, NULL, NULL, NULL, NULL),
(32, 26, 2, 1, '2023-09-18', NULL, 'PC service', 'replace power supply unit\n', 1.00, 100.00, NULL, 3, NULL, NULL, NULL, NULL),
(33, 27, 2, 11, '2023-09-25', NULL, 'Crucial BX500 2TB 3D NAND SATA 2.5in SSD', '', 1.00, 145.00, 14.50, 1, NULL, NULL, NULL, NULL),
(36, 27, 2, 2, '2023-09-25', NULL, 'Orico 2.5 Inch Hard Drive Adapter', 'Turns your 2.5 inch SATA HDD / SSD into 3.5 inch so you can install it into your desktop PC', 1.00, 20.00, 2.00, 2, NULL, NULL, NULL, NULL),
(35, 27, 2, 1, '2023-09-25', NULL, 'PC service', 'Install new SSD and reinstall Windows 10.\nRecover data and applications.', 2.00, 100.00, NULL, 3, NULL, NULL, NULL, NULL),
(37, 28, 2, 13, '2023-10-08', NULL, 'Crucial MX500 1TB 3D 6Gbps 2.5in SSD 560MB/s 510MB/s NAND SATA SSD', '', 1.00, 82.00, NULL, 1, NULL, NULL, NULL, NULL),
(38, 28, 2, 2, '2023-10-08', NULL, 'Orico 2.5 Inch Hard Drive Adapter', 'Turns your 2.5 inch SATA HDD / SSD into 3.5 inch so you can install it into your desktop PC', 1.00, 20.00, NULL, 2, NULL, NULL, NULL, NULL),
(39, 28, 2, 9, '2023-10-08', NULL, 'hours service home', 'image HD to new SSD\nand install into HP AIO computer\nassist with system ', 1.50, 50.00, NULL, 3, NULL, NULL, NULL, NULL),
(40, 28, 2, 10, '2023-10-08', NULL, 'Vision Australia Keyboard', '', 1.00, 15.00, NULL, 4, NULL, NULL, NULL, NULL),
(41, 29, 2, 1, '2023-10-10', NULL, 'PC service', 'Assist with cashflow manager backups, outlook, and Onedrive sync, check power options', 1.00, 100.00, NULL, 1, NULL, NULL, NULL, NULL),
(44, 31, 2, NULL, '2023-12-28', NULL, 'Computer System', 'Cooler Master MasterBox Q500L ATX Case\nMSI B550 MS-7C85 motherboard\n32-GB RAM\n1x 512GB NVME\n1x 256GM NVME\nRyzen 5 APU ', 1.00, 300.00, NULL, 1, NULL, NULL, NULL, NULL),
(45, 31, 2, NULL, '2023-12-28', NULL, 'Creative Pebble Speakers', '', 1.00, 30.00, NULL, 2, NULL, NULL, NULL, NULL),
(46, 32, 2, NULL, '2024-01-05', NULL, 'Kingston 16GB (1x16GB) KVR32S22D8/16 3200MHz DDR4 SODIMM RAM', '16 gigabyte RAM (memory) upgrade for laptop', 1.00, 50.00, NULL, 1, NULL, NULL, NULL, NULL),
(47, 32, 2, NULL, '2024-01-05', NULL, '280 SSD heat sink', 'heat sink for full length SSD module for Dell laptop', 1.00, 28.00, NULL, 2, NULL, NULL, NULL, NULL),
(48, 32, 2, NULL, '2024-01-05', NULL, '512GB NVMe drive', 'Drive that Windows 11 was installed on', 1.00, 40.00, NULL, 3, NULL, NULL, NULL, NULL),
(49, 33, 2, 20, '2024-02-15', NULL, 'Leader Corporate S43 Slim Desktop, Intel i7-12700, 16GB RAM, 500GB M.2 NVMe SSD, 300W GOLD 80+ PSU, Windows 11 Pro, 3 Years \"4 Hour\" Onsite Warranty', 'DESCRIPTION\n\nCPU\nIntel® 12th Generation Core i7-12700 12-Cores 20-Threads\n\nMainboard\nAsus Corporate Server grade \"Pro\" Intel B660M-C/CSM-S with 24/7 stability and reliability\n\nGraphics\nIntel HD graphics 730. Supports up to 3 displays simultaneously via 2x DP, 1x HDMI and 1x D-SUB\n\nMemory\n16GB (1x 16GB) DDR4 UDIMM RAM\n\nOptical\n24X DVD+/-R/RW DVD Burner with software\n\nStorage\n500GB M.2 NVMe SSD\n\nCase\nLeader mATX slimline Black Case. Advanced cooling and noise reduction features. Gold 80+ 300W PSU\n\nKeyboard & Mouse\nWired Full Size Keyboard and Mouse\n\nOperating System\nMicrosoft Windows 11 Professional\n\nEthernet\nGigabit LAN\n\nInputs/Outputs\n2x USB 3.2 Gen 1 ports (2 x Type-A), 2x USB 2.0 ports (2 x Type-A), 2x DisplayPort, 1x HDMI® port, 1x D-Sub port , 1x Intel® 1Gb Ethernet port , 3x Audio jacks, 1x PS/2 keyboard (purple) port , 1x PS/2 mouse (green) port\n\nDimensions\n95x280x360mm (W/H/D)\n\nWarranty\n3 Years 4 Hour \"Leader Up and Running\" Australia Wide Onsite Warranty. 4 Hours is from time call logged during business hours Monday to Friday 9am - 5.30pm in metro areas only.\n', 2.00, 1600.00, NULL, 1, NULL, NULL, NULL, NULL),
(50, 33, 2, 16, '2024-02-15', NULL, 'HP E24i G4 23.8\"/24\" WUXGA IPS Monitor Anti-Glare 1920x1200 DisplayPort VGA HDMI Tilt Swivel Pivot USB Hub 3yrs Wty', 'DESCRIPTION\n\nHP E24i G4 24\" WUXGA IPS 1920 x 1200 DisplayPort, VGA, HDMI, Tilt, Swivel, Pivot, USB, 3 YR WTY MONITOR (9VJ40AA)\n\nProduct specifications\n\nDisplay type IPS\n\nDisplay features Low blue light mode; Anti-glare\n\nOnscreen controls Brightness; Exit; Information; Management; Power control; Input control; Menu control; Image; Color\n\nNative resolution WUXGA (1920 x 1200)\n\nResolutions supported 1024 x 768; 1280 x 1024; 1280 x 720; 1280 x 800; 1440 x 900; 1600 x 900; 1680 x 1050; 1920 x 1080; 1920 x 1200; 640 x 480; 720 x 400; 800 x 600\n\nContrast ratio 1000:1\n\nBrightness 250 nits\n\nPixel pitch 0.27 mm\n\nSignal input connectors 1 VGA; 1 USB Type-B; 1 DisplayPort™ 1.2 (with HDCP support); 1 HDMI 1.4 (with HDCP support); 4 USB-A 3.2 Gen 1\n\nWebcam No integrated camera\n\nVESA Mounting 100 mm x 100 mm\n\nPower supply Input voltage 100 to 240 VAC\n\nDimensions (W X D X H) 20.94 x 1.85 x 13.88 in Without stand.\n\nWeight 13.36 lb\n\nWhat\'s in the box Monitor; DisplayPort™ 1.2 cable; HDMI cable; USB cable; QSP; AC power cable; Doc-kit\n', 4.00, 309.00, NULL, 2, NULL, NULL, NULL, NULL),
(51, 33, 2, 17, '2024-02-15', NULL, 'M365 - Microsoft 365 Business Standard (New Commerce) 12 months subscription', 'Desktop, web, and mobile versions of Word, Excel, PowerPoint, and Outlook\n\nCustom business email (you@yourbusiness.com)\n\nChat, call, collaborate, meet online, and host webinars up to 300 attendees\n\n1 TB of cloud storage per use\n\nVideo editing and design tools with Clipchamp\n', 2.00, 224.40, NULL, 3, NULL, NULL, NULL, NULL),
(52, 33, 2, 18, '2024-02-15', NULL, 'MFC-L8390CDW *NEW*Compact Colour Laser Multi-Function Centre - Print/Scan/Copy/FAX with Print speeds of Up to 30 ppm, 2-Sided Printing & Scanning', 'DESCRIPTION\n\nBrother MFC-L8390CDW *NEW*Compact Colour Laser Multi-Function Centre - Print/Scan/Copy/FAX with Print speeds of Up to 30 ppm, 2-Sided Printing & Scanning, Wired & Wireless networking, ADF, 3.5” Touch Screen', 1.00, 700.00, NULL, 4, NULL, NULL, NULL, NULL),
(53, 33, 2, 1, '2024-02-15', NULL, 'PC service', 'Setup new computers and printer, migrate data, setup office and e-mail', 4.00, 100.00, NULL, 5, NULL, NULL, NULL, NULL),
(54, 34, 2, 1, '2024-02-19', NULL, 'PC service', 'configure e-mail and software on computers, setup one drive\nsetup macrium reflect backup\nsetup printer/scanner\nsetup network switch', 4.00, 100.00, NULL, 1, NULL, NULL, NULL, NULL),
(55, 35, 2, 9, '2024-02-23', NULL, 'hours service home', 'assist with printer and scanner, run scan with Malware bytes, check updates', 1.00, 50.00, NULL, 1, NULL, NULL, NULL, NULL),
(56, 36, 2, 13, '2024-02-26', NULL, 'Crucial MX500 1TB 3D 6Gbps 2.5in SSD 560MB/s 510MB/s NAND SATA SSD', 'Solid state drive used to upgrade Toshiba All in One computer', 1.00, 100.00, NULL, 1, NULL, NULL, NULL, NULL),
(57, 36, 2, 22, '2024-02-26', NULL, 'Logitech Z150 2.0 Stereo Speakers', 'Logitech Z150 2.0 Stereo Speakers 6W Compact Size Easily Access to Power & Volume Control Headphone & Auxiliary Jack for TV PC Smartphone Tablet', 2.00, 45.00, NULL, 2, NULL, NULL, NULL, NULL),
(58, 37, 0, 14, '2024-03-03', NULL, 'dvi to display port cable', '', 1.00, 10.00, NULL, 1, NULL, NULL, NULL, NULL),
(59, 39, 2, 25, '2024-03-05', NULL, 'Reflect 8 Workstation with Premium Support (one time purchase)', 'Macrium Reflect backup software one time purchase. Product support is limited to the first year unless renewed.', 1.00, 232.82, NULL, 1, NULL, NULL, NULL, NULL),
(60, 39, 2, 24, '2024-03-05', NULL, 'Verbatim 2TB 2.5\" USB 3.0 Black Store\'n\'Go HDD Grid Design', 'External drive for computer backup. Large capacity of 2TB.', 1.00, 130.00, NULL, 2, NULL, NULL, NULL, NULL),
(61, 39, 2, 1, '2024-03-05', NULL, 'PC service', 'Onsite setup to activate software license\n\nand install backup drive.', 1.00, 100.00, NULL, 3, NULL, NULL, NULL, NULL),
(62, 40, 2, 4, '2024-03-06', NULL, 'Kingston 1TB NV2 2280 NVMe SSD', '', 1.00, 70.00, NULL, 1, NULL, NULL, NULL, NULL),
(63, 40, 2, 1, '2024-03-06', NULL, 'PC service', 'Install NVMe drive in computer and install Ubuntu Linux.', 1.00, 100.00, NULL, 2, NULL, NULL, NULL, NULL),
(64, 41, 2, 4, '2024-03-06', NULL, 'Kingston 1TB NV2 2280 NVMe SSD', 'Kingston NV2 1TB PCIe 4.0 M.2 2280 NVMe SSD (SNV2S/1000G)', 1.00, 70.00, NULL, 1, NULL, NULL, NULL, NULL),
(65, 41, 2, 1, '2024-03-06', NULL, 'PC service', 'Install NVMe drive in computer and install Ubuntu Linux.', 1.00, 100.00, NULL, 2, NULL, NULL, NULL, NULL),
(66, 42, 2, 14, '2024-03-07', NULL, 'dvi to display port cable', 'yr', 1.00, 10.00, NULL, 1, NULL, NULL, NULL, NULL),
(67, 43, 2, 9, '2024-03-08', NULL, 'hours service home', 'Installed bitdefender AV, registered softmaker, did Windows updates, updated itunes, setup WiFi printer and tested printing ', 1.00, 50.00, NULL, 1, NULL, NULL, NULL, NULL),
(68, 44, 2, 13, '2024-03-08', NULL, 'Crucial MX500 1TB 3D 6Gbps 2.5in SSD 560MB/s 510MB/s NAND SATA SSD', 'new Solid state drive (C drive)', 1.00, 100.00, NULL, 1, NULL, NULL, NULL, NULL),
(69, 44, 2, 26, '2024-03-08', NULL, '24 Pin to 14 Pin PSU ATX Main Power Supply Adapter', 'adapter for proprietary Lenovo power supply', 1.00, 4.00, NULL, 2, NULL, NULL, NULL, NULL),
(70, 44, 2, 9, '2024-03-08', NULL, 'hours service home', 'Install replacement PSU (power supply unit) and adapter as well as new solid state drive. Transfer data accross.', 2.00, 50.00, NULL, 3, NULL, NULL, NULL, NULL),
(71, 45, 2, 9, '2024-03-08', NULL, 'hours service home', '', 1.00, 50.00, NULL, 1, NULL, NULL, NULL, NULL),
(72, 46, 2, 1, '2024-03-11', NULL, 'PC service', 'Assist with setup of Reckon multi-user. Configure Windows networking and sharing. Setup AV software. Setup of Avast business on two machines.', 4.00, 100.00, NULL, 1, NULL, NULL, NULL, NULL),
(73, 47, 2, 9, '2024-03-13', NULL, 'hours service home', 'Assist with emailing in Outlook. Configure Google chrome.\nRan scan with malwarebytes.\nRemoved driver one.\nPerforomed Windows updates.', 1.00, 50.00, NULL, 1, NULL, NULL, NULL, NULL),
(74, 48, 2, 9, '2024-04-10', NULL, 'hours service home', 'troubleshoot printer, update windows, install bitfender antivirus', 1.00, 50.00, NULL, 1, NULL, NULL, NULL, NULL),
(75, 49, 2, 27, '2024-04-16', NULL, 'Epson Expression XP-6100 MFC Printer', 'Epson MFC printer', 1.00, 159.00, NULL, 1, NULL, NULL, NULL, NULL),
(76, 50, 2, 28, '2024-05-02', NULL, 'Corsair  16GB (2x8GB) 3000Mhz DDR4 RAM', 'Corsair Vengeance LPX 16GB (2x8GB) 3000Mhz DDR4 RAM', 1.00, 68.00, NULL, 1, NULL, NULL, NULL, NULL),
(77, 50, 2, 1, '2024-05-02', NULL, 'PC service', 'Install new RAM\ntroubleshoot internet problem in Edge and Chrome\nInstalled firefox\nUpdate Dell BIOS', 2.00, 100.00, NULL, 2, NULL, NULL, NULL, NULL),
(78, 51, 2, 1, '2024-05-10', NULL, 'PC service', 'setup new Asus laptop\nsetup emclient\ninstall softmaker office\nsetup printer', 1.00, 100.00, NULL, 1, NULL, NULL, NULL, NULL),
(79, 53, 2, 10, '2024-05-23', NULL, 'Vision Australia Keyboard', '', 1.00, 30.00, NULL, 1, NULL, NULL, NULL, NULL),
(80, 53, 2, 9, '2024-05-23', NULL, 'hours service home', 'install Vision Australia keyboard\nassist with sign-in to computer and reset Microsoft account password.\nSetup pin to login to computer.', 1.00, 50.00, NULL, 2, NULL, NULL, NULL, NULL),
(81, 54, 2, 9, '2024-06-04', NULL, 'hours service home', 'repair profile on Windows laptop\nto get Office working\ninstalled PC manager to optimise computer\ninstalled emails client on HP AIO', 2.00, 50.00, NULL, 1, NULL, NULL, NULL, NULL),
(88, 59, 2, 9, '2024-07-10', NULL, 'hours service home', 'Setup new Lenovo laptop,\ncopy data across,\nsetup Office and outlook,\nsetup printer', 3.00, 50.00, NULL, 1, NULL, NULL, NULL, NULL),
(83, 56, 2, 29, '2024-06-17', NULL, 'half hour remote IT support', 'assist with google chrome extensions issue over teamviewer\nremoved extensions sub-folders and restarted chrome.\nRemoved unneeded extensions.\nAdvised on use of backup and AV software.', 1.00, 30.00, NULL, 1, NULL, NULL, NULL, NULL),
(84, 57, 2, 9, '2024-06-18', NULL, 'hours service home', 'install RAM and SSD drive and reinstall Windows 10', 1.00, 50.00, NULL, 1, NULL, NULL, NULL, NULL),
(85, 57, 2, 30, '2024-06-18', NULL, 'Silicon Power Ace A55 256GB TLC 3D NAND 2.5in SATA III SSD', '', 1.00, 40.00, NULL, 2, NULL, NULL, NULL, NULL),
(86, 57, 2, 2, '2024-06-18', NULL, 'Orico 2.5 Inch Hard Drive Adapter', 'Turns your 2.5 inch SATA HDD / SSD into 3.5 inch so you can install it into your desktop PC', 1.00, 20.00, NULL, 3, NULL, NULL, NULL, NULL),
(87, 58, 2, 1, '2024-06-20', NULL, 'PC service', 'reinstall onedrive,\n setup firewall rules for reckon\nupdate macrium reflect and run backup', 1.00, 100.00, NULL, 1, NULL, NULL, NULL, NULL),
(89, 60, 2, 1, '2024-07-22', NULL, 'PC service', 'Setup new Dell computer.\nTransfer data from previous computer. Setup E-mail, one note and cash flow manager. Setup printer.', 4.00, 100.00, NULL, 1, NULL, NULL, NULL, NULL),
(90, 61, 2, 1, '2024-07-29', NULL, 'PC service', 'setup printer and scanner\nconfigure eml viewer for one note\nconfigure backups', 2.00, 100.00, NULL, 1, NULL, NULL, NULL, NULL),
(91, 61, 2, 1, '2024-07-29', NULL, 'PC service', 'install Windows 11 on Dell for Paul', 1.00, 100.00, NULL, 2, NULL, NULL, NULL, NULL),
(92, 61, 2, 9, '2024-07-29', NULL, 'hours service home', 'Setup accounts and MS office for Paul', 2.00, 50.00, NULL, 3, NULL, NULL, NULL, NULL),
(93, 61, 2, 31, '2024-07-29', NULL, 'Crucial P3 PCIe Gen3 NVMe M.2 SSD - 500GB', 'Faster storage device NVMe', 1.00, 65.00, NULL, 4, NULL, NULL, NULL, NULL),
(94, 61, 2, 32, '2024-07-29', NULL, 'TP-LINK 8-port Desktop Gigabit Switch', '8 10/100/1000M RJ45 ports, plastic case (TL-SG1008D)', 1.00, 35.00, NULL, 5, NULL, NULL, NULL, NULL),
(97, 62, 2, 29, '2024-08-13', NULL, 'half hour remote IT support', 'assist with installing office 365, assist with backup of email folders and archive, assist with management of folders on Telstra webmail, assist with setup of external screen in extended mode', 2.00, 30.00, NULL, 1, NULL, NULL, NULL, NULL),
(96, 61, 2, 33, '2024-07-29', NULL, 'DVI-D Dual Link M-M Cable', 'DVI cable', 1.00, 5.00, NULL, 6, NULL, NULL, NULL, NULL),
(98, 63, 2, 1, '2024-08-15', NULL, 'PC service', 'setup new wifi modem and voip\nsetup msg viewer for onenote\nsetup soundbars', 2.41, 100.00, NULL, 1, NULL, NULL, NULL, NULL),
(99, 63, 2, 35, '2024-08-15', NULL, 'Creative Stage SE Mini Speakers Sound Bar ', 'Creative Stage SE Mini Speakers Sound Bar ', 1.00, 80.00, NULL, 2, NULL, NULL, NULL, NULL),
(100, 63, 2, 34, '2024-08-15', NULL, 'TP-Link AC2100 Wireless Modem Router', 'TP-Link AC2100 Wireless MU-MIMO Modem Router', 1.00, 224.45, NULL, 3, NULL, NULL, NULL, NULL),
(101, 64, 2, 38, '2024-08-28', NULL, 'hour IT support A1', '', 1.00, 220.00, NULL, 1, NULL, NULL, NULL, NULL),
(102, 65, 2, 1, '2024-09-12', NULL, 'PC service', 'Configure MFA for Microsoft account and fix Thunderbird email.\nSetup emclient as backup.', 1.00, 100.00, NULL, 1, NULL, NULL, NULL, NULL),
(103, 66, 2, 40, '2024-09-13', NULL, 'Thermaltake 650W Smart Pro RGB', 'Thermaltake 650W Smart Pro RGB Bronze Fully Modular Power Supply', 1.00, 100.00, NULL, 1, NULL, NULL, NULL, NULL),
(104, 66, 2, 13, '2024-09-13', NULL, 'Crucial MX500 1TB 3D 6Gbps 2.5in SSD 560MB/s 510MB/s NAND SATA SSD', 'Faster harddrive (solid state)', 1.00, 100.00, NULL, 2, NULL, NULL, NULL, NULL),
(105, 66, 2, 1, '2024-09-13', NULL, 'PC service', 'upgrade computer, install new PSU, install new HD, image from previous drive.', 2.00, 100.00, NULL, 3, NULL, NULL, NULL, NULL),
(106, 67, 2, 40, '2024-09-14', NULL, 'Thermaltake 650W Smart Pro RGB', 'Thermaltake 650W Smart Pro RGB Bronze Fully Modular Power Supply', 1.00, 100.00, NULL, 1, NULL, NULL, NULL, NULL),
(107, 67, 2, 13, '2024-09-14', NULL, 'Crucial MX500 1TB 3D 6Gbps 2.5in SSD 560MB/s 510MB/s NAND SATA SSD', 'Faster harddrive (solid state)', 1.00, 100.00, NULL, 2, NULL, NULL, NULL, NULL),
(108, 67, 2, 1, '2024-09-14', NULL, 'PC service', 'upgrade computer, install new PSU, install new HD, image from previous drive.', 2.00, 100.00, NULL, 3, NULL, NULL, NULL, NULL),
(109, 68, 2, 1, '2024-09-19', NULL, 'PC service', 'setup printer,\nsetup email accounts in thunderbird\nassist with password reset\nassist with setup of security and account recover options ', 1.00, 100.00, NULL, 1, NULL, NULL, NULL, NULL),
(110, 69, 2, NULL, '2024-09-30', NULL, '512 Gb Nvme', 'new hard-drive for laptop', 1.00, 97.27, NULL, 1, NULL, NULL, NULL, NULL),
(111, 69, 2, 1, '2024-09-30', NULL, 'PC service', 'install new hard-drive in Dell XPS laptop\nrestore data from old drive', 1.00, 100.00, NULL, 2, NULL, NULL, NULL, NULL),
(112, 70, 0, 9, '2024-11-08', NULL, 'hours service home', 'install RAM and new NVME drive\nreinstall Windows 11\nrestore files and\ncomplete setup', 2.00, 50.00, NULL, 1, NULL, NULL, NULL, NULL),
(113, 70, 0, 41, '2024-11-08', NULL, 'Kingston NV2 500GB NVMe SSD', 'Kingston NV2 500GB PCIe 4.0 M.2 2280 NVMe SSD', 1.00, 55.00, NULL, 2, NULL, NULL, NULL, NULL),
(114, 70, 0, 42, '2024-11-08', NULL, '16 GB DDR4 SO-DIMM', 'laptop RAM upgrade', 1.00, 50.00, NULL, 3, NULL, NULL, NULL, NULL),
(115, 71, 0, 1, '2024-11-11', NULL, 'PC service', 'Backup data and perform clean reinstall of Lenovo laptop.\nRestore Microsoft account.', 1.00, 100.00, NULL, 1, NULL, NULL, NULL, NULL),
(116, 72, 0, 9, '2024-12-13', NULL, 'hours service home', 'printer troubleshooting', 1.00, 50.00, NULL, 1, NULL, NULL, NULL, NULL),
(117, 73, 2, 1, '2025-01-20', NULL, 'PC service', 'Assist with chrome update', 0.25, 100.00, NULL, 1, NULL, NULL, NULL, NULL),
(118, 74, 2, 1, '2025-01-28', NULL, 'PC service', 'assist with backups of computer and e-maiil to new drive\nassist with recovery of lost e-mails from backup image ost file\n', 3.00, 100.00, NULL, 1, NULL, NULL, NULL, NULL),
(119, 75, 2, 1, '2025-02-11', NULL, 'PC service', 'Setup wifi networking on printer. Test printing OK. Standard consult.', 1.00, 100.00, NULL, 1, NULL, NULL, NULL, NULL),
(120, 76, 2, 43, '2025-02-22', NULL, 'Lenovo Tab M11 WiFi', 'tablet for e-mail', 1.00, 300.00, NULL, 1, NULL, NULL, NULL, NULL),
(121, 77, 2, 1, '2025-03-04', NULL, 'PC service', 'Upgrade computer to Windows 11', 1.00, 100.00, NULL, 1, NULL, NULL, NULL, NULL),
(122, 79, 2, 45, '2025-05-03', NULL, 'Corsair 16GB (2x8GB) 2666Mhz DDR4 RAM', 'DDR RAM for new motherboard', 1.00, 60.00, NULL, 1, NULL, NULL, NULL, NULL),
(123, 79, 2, 44, '2025-05-03', NULL, 'MSI B550-A PRO AM4 ATX Motherboard (B550-A PRO)', 'MSI motherboard for system upgrade to support Windows 11', 1.00, 166.00, NULL, 2, NULL, NULL, NULL, NULL),
(124, 79, 2, 1, '2025-05-03', NULL, 'PC service', 'upgrade PC, Install Windows 11, restore data, complete setup', 3.00, 100.00, NULL, 3, NULL, NULL, NULL, NULL),
(125, 80, 2, 1, '2025-05-27', NULL, 'PC service (apple)', 'Assist with setup of new apple computers. Computer data across.\nRemove old drives from devices. ', 2.00, 100.00, NULL, 1, NULL, NULL, NULL, NULL),
(126, 81, 2, 29, '2025-06-16', NULL, 'half hour remote IT support', 'setup and support for Microsoft teams meeting over team viewer.', 3.00, 30.00, NULL, 1, NULL, NULL, NULL, NULL),
(127, 82, 2, 1, '2025-06-24', NULL, 'PC service', 'Setup screen, configure printer, assist with e-mail and domain name recovery.', 1.00, 100.00, NULL, 1, NULL, NULL, NULL, NULL),
(128, 89, 2, 1, '2025-10-04', NULL, 'PC service', 'Diagnose existing HP computer. Setup new PC.\nSetup accounts, setup MS office, setup e-mail. Restore data from old machine. Setup Brother network printer.', 5.00, 100.00, NULL, 1, NULL, NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `ip_invoice_item_amounts`
--

CREATE TABLE `ip_invoice_item_amounts` (
  `item_amount_id` int(11) NOT NULL,
  `item_id` int(11) NOT NULL,
  `item_subtotal` decimal(20,2) DEFAULT NULL,
  `item_tax_total` decimal(20,2) DEFAULT NULL,
  `item_discount` decimal(20,2) DEFAULT NULL,
  `item_total` decimal(20,2) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `ip_invoice_item_amounts`
--

INSERT INTO `ip_invoice_item_amounts` (`item_amount_id`, `item_id`, `item_subtotal`, `item_tax_total`, `item_discount`, `item_total`) VALUES
(1, 1, 20.00, 0.00, 0.00, 20.00),
(2, 2, 25.00, 0.00, 0.00, 25.00),
(7, 7, 25.00, 0.00, 0.00, 25.00),
(8, 8, 100.00, 10.00, 0.00, 110.00),
(9, 9, 200.00, 20.00, 0.00, 220.00),
(10, 10, 240.00, 24.00, 0.00, 264.00),
(11, 11, 70.00, 7.00, 0.00, 77.00),
(14, 14, 67.00, 6.70, 0.00, 73.70),
(13, 13, 100.00, 10.00, 0.00, 110.00),
(15, 15, 179.00, 17.90, 0.00, 196.90),
(16, 16, 54.90, 5.49, 0.00, 60.39),
(17, 17, 50.00, 5.00, 0.00, 55.00),
(18, 18, 110.00, 11.00, 0.00, 121.00),
(19, 19, 75.00, 7.50, 0.00, 82.50),
(20, 20, 67.00, 6.70, 0.00, 73.70),
(21, 21, 100.00, 10.00, 0.00, 110.00),
(22, 22, 15.00, 1.50, 0.00, 16.50),
(23, 23, 50.00, 5.00, 0.00, 55.00),
(42, 42, 10.00, 1.00, 0.00, 11.00),
(25, 25, 50.00, 5.00, 0.00, 55.00),
(27, 27, 145.00, 0.00, 0.00, 145.00),
(28, 28, 20.00, 0.00, 0.00, 20.00),
(29, 29, 200.00, 20.00, 0.00, 220.00),
(30, 30, 0.00, 0.00, 0.00, 0.00),
(31, 31, 106.00, 10.60, 0.00, 116.60),
(32, 32, 100.00, 10.00, 0.00, 110.00),
(33, 33, 145.00, 14.50, 14.50, 145.00),
(36, 36, 20.00, 2.00, 2.00, 20.00),
(35, 35, 200.00, 20.00, 0.00, 220.00),
(37, 37, 82.00, 8.20, 0.00, 90.20),
(38, 38, 20.00, 2.00, 0.00, 22.00),
(39, 39, 75.00, 7.50, 0.00, 82.50),
(40, 40, 15.00, 1.50, 0.00, 16.50),
(41, 41, 100.00, 10.00, 0.00, 110.00),
(43, 43, 50.00, 5.00, 0.00, 55.00),
(44, 44, 300.00, 30.00, 0.00, 330.00),
(45, 45, 30.00, 3.00, 0.00, 33.00),
(46, 46, 50.00, 5.00, 0.00, 55.00),
(47, 47, 28.00, 2.80, 0.00, 30.80),
(48, 48, 40.00, 4.00, 0.00, 44.00),
(49, 49, 3200.00, 320.00, 0.00, 3520.00),
(50, 50, 1236.00, 123.60, 0.00, 1359.60),
(51, 51, 448.80, 44.88, 0.00, 493.68),
(52, 52, 700.00, 70.00, 0.00, 770.00),
(53, 53, 400.00, 40.00, 0.00, 440.00),
(54, 54, 400.00, 40.00, 0.00, 440.00),
(55, 55, 50.00, 5.00, 0.00, 55.00),
(56, 56, 100.00, 10.00, 0.00, 110.00),
(57, 57, 90.00, 9.00, 0.00, 99.00),
(58, 58, 10.00, 0.00, 0.00, 10.00),
(59, 59, 232.82, 23.28, 0.00, 256.10),
(60, 60, 130.00, 13.00, 0.00, 143.00),
(61, 61, 100.00, 10.00, 0.00, 110.00),
(62, 62, 70.00, 7.00, 0.00, 77.00),
(63, 63, 100.00, 10.00, 0.00, 110.00),
(64, 64, 70.00, 7.00, 0.00, 77.00),
(65, 65, 100.00, 10.00, 0.00, 110.00),
(66, 66, 10.00, 1.00, 0.00, 11.00),
(67, 67, 50.00, 5.00, 0.00, 55.00),
(68, 68, 100.00, 10.00, 0.00, 110.00),
(69, 69, 4.00, 0.40, 0.00, 4.40),
(70, 70, 100.00, 10.00, 0.00, 110.00),
(71, 71, 50.00, 5.00, 0.00, 55.00),
(72, 72, 400.00, 40.00, 0.00, 440.00),
(73, 73, 50.00, 5.00, 0.00, 55.00),
(74, 74, 50.00, 5.00, 0.00, 55.00),
(75, 75, 159.00, 15.90, 0.00, 174.90),
(76, 76, 68.00, 6.80, 0.00, 74.80),
(77, 77, 200.00, 20.00, 0.00, 220.00),
(78, 78, 100.00, 10.00, 0.00, 110.00),
(79, 79, 30.00, 3.00, 0.00, 33.00),
(80, 80, 50.00, 5.00, 0.00, 55.00),
(81, 81, 100.00, 10.00, 0.00, 110.00),
(88, 88, 150.00, 15.00, 0.00, 165.00),
(83, 83, 30.00, 3.00, 0.00, 33.00),
(84, 84, 50.00, 5.00, 0.00, 55.00),
(85, 85, 40.00, 4.00, 0.00, 44.00),
(86, 86, 20.00, 2.00, 0.00, 22.00),
(87, 87, 100.00, 10.00, 0.00, 110.00),
(89, 89, 400.00, 40.00, 0.00, 440.00),
(90, 90, 200.00, 20.00, 0.00, 220.00),
(91, 91, 100.00, 10.00, 0.00, 110.00),
(92, 92, 100.00, 10.00, 0.00, 110.00),
(93, 93, 65.00, 6.50, 0.00, 71.50),
(94, 94, 35.00, 3.50, 0.00, 38.50),
(97, 97, 60.00, 6.00, 0.00, 66.00),
(96, 96, 5.00, 0.50, 0.00, 5.50),
(98, 98, 241.00, 24.10, 0.00, 265.10),
(99, 99, 80.00, 8.00, 0.00, 88.00),
(100, 100, 224.45, 22.45, 0.00, 246.90),
(101, 101, 220.00, 22.00, 0.00, 242.00),
(102, 102, 100.00, 10.00, 0.00, 110.00),
(103, 103, 100.00, 10.00, 0.00, 110.00),
(104, 104, 100.00, 10.00, 0.00, 110.00),
(105, 105, 200.00, 20.00, 0.00, 220.00),
(106, 106, 100.00, 10.00, 0.00, 110.00),
(107, 107, 100.00, 10.00, 0.00, 110.00),
(108, 108, 200.00, 20.00, 0.00, 220.00),
(109, 109, 100.00, 10.00, 0.00, 110.00),
(110, 110, 97.27, 9.73, 0.00, 107.00),
(111, 111, 100.00, 10.00, 0.00, 110.00),
(112, 112, 100.00, 0.00, 0.00, 100.00),
(113, 113, 55.00, 0.00, 0.00, 55.00),
(114, 114, 50.00, 0.00, 0.00, 50.00),
(115, 115, 100.00, 0.00, 0.00, 100.00),
(116, 116, 50.00, 0.00, 0.00, 50.00),
(117, 117, 25.00, 2.50, 0.00, 27.50),
(118, 118, 300.00, 30.00, 0.00, 330.00),
(119, 119, 100.00, 10.00, 0.00, 110.00),
(120, 120, 300.00, 30.00, 0.00, 330.00),
(121, 121, 100.00, 10.00, 0.00, 110.00),
(122, 122, 60.00, 6.00, 0.00, 66.00),
(123, 123, 166.00, 16.60, 0.00, 182.60),
(124, 124, 300.00, 30.00, 0.00, 330.00),
(125, 125, 200.00, 20.00, 0.00, 220.00),
(126, 126, 90.00, 9.00, 0.00, 99.00),
(127, 127, 100.00, 10.00, 0.00, 110.00),
(128, 128, 500.00, 50.00, 0.00, 550.00);

-- --------------------------------------------------------

--
-- Table structure for table `ip_invoice_sumex`
--

CREATE TABLE `ip_invoice_sumex` (
  `sumex_id` int(11) NOT NULL,
  `sumex_invoice` int(11) NOT NULL,
  `sumex_reason` int(11) NOT NULL,
  `sumex_diagnosis` varchar(500) NOT NULL,
  `sumex_observations` varchar(500) NOT NULL,
  `sumex_treatmentstart` date NOT NULL,
  `sumex_treatmentend` date NOT NULL,
  `sumex_casedate` date NOT NULL,
  `sumex_casenumber` varchar(35) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `ip_invoice_tax_rates`
--

CREATE TABLE `ip_invoice_tax_rates` (
  `invoice_tax_rate_id` int(11) NOT NULL,
  `invoice_id` int(11) NOT NULL,
  `tax_rate_id` int(11) NOT NULL,
  `include_item_tax` int(1) NOT NULL DEFAULT 0,
  `invoice_tax_rate_amount` decimal(10,2) NOT NULL DEFAULT 0.00
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `ip_item_lookups`
--

CREATE TABLE `ip_item_lookups` (
  `item_lookup_id` int(11) NOT NULL,
  `item_name` varchar(100) NOT NULL DEFAULT '',
  `item_description` longtext NOT NULL,
  `item_price` decimal(10,2) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `ip_login_log`
--

CREATE TABLE `ip_login_log` (
  `login_name` varchar(100) NOT NULL,
  `log_count` int(11) DEFAULT 0,
  `log_create_timestamp` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `ip_merchant_responses`
--

CREATE TABLE `ip_merchant_responses` (
  `merchant_response_id` int(11) NOT NULL,
  `invoice_id` int(11) NOT NULL,
  `merchant_response_successful` tinyint(1) DEFAULT 1,
  `merchant_response_date` date NOT NULL,
  `merchant_response_driver` varchar(35) NOT NULL,
  `merchant_response` varchar(255) NOT NULL,
  `merchant_response_reference` varchar(255) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `ip_payments`
--

CREATE TABLE `ip_payments` (
  `payment_id` int(11) NOT NULL,
  `invoice_id` int(11) NOT NULL,
  `payment_method_id` int(11) NOT NULL DEFAULT 0,
  `payment_date` date NOT NULL,
  `payment_amount` decimal(20,2) DEFAULT NULL,
  `payment_note` longtext NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `ip_payments`
--

INSERT INTO `ip_payments` (`payment_id`, `invoice_id`, `payment_method_id`, `payment_date`, `payment_amount`, `payment_note`) VALUES
(1, 2, 3, '2022-12-14', 45.00, ''),
(2, 6, 3, '2023-01-08', 25.00, ''),
(3, 13, 3, '2023-05-03', 220.00, ''),
(4, 17, 3, '2023-05-12', 257.29, ''),
(5, 14, 3, '2023-05-12', 341.00, ''),
(6, 19, 3, '2023-05-31', 121.00, ''),
(7, 20, 3, '2023-06-19', 82.50, ''),
(8, 21, 3, '2023-06-22', 183.70, ''),
(9, 25, 1, '2023-09-14', 385.00, ''),
(10, 26, 3, '2023-09-23', 226.60, ''),
(11, 27, 1, '2023-09-14', 385.00, ''),
(12, 28, 3, '2023-10-10', 211.20, ''),
(13, 29, 3, '2023-10-30', 110.00, ''),
(14, 24, 1, '2023-10-30', 55.00, ''),
(15, 22, 1, '2023-10-30', 71.50, ''),
(16, 30, 3, '2023-12-28', 66.00, ''),
(17, 31, 3, '2023-12-28', 363.00, ''),
(18, 32, 3, '2024-01-06', 129.80, ''),
(19, 33, 3, '2024-02-19', 6583.28, ''),
(20, 34, 3, '2024-02-19', 440.00, ''),
(21, 35, 3, '2024-02-23', 55.00, ''),
(22, 36, 3, '2024-03-02', 209.00, ''),
(23, 39, 3, '2024-03-06', 509.10, ''),
(24, 44, 3, '2024-03-08', 224.40, ''),
(25, 43, 1, '2024-03-08', 55.00, ''),
(26, 45, 1, '2024-03-08', 55.00, ''),
(27, 46, 3, '2024-03-12', 440.00, ''),
(28, 47, 3, '2024-03-24', 55.00, ''),
(29, 49, 3, '2024-04-21', 174.90, ''),
(30, 48, 3, '2024-04-25', 55.00, ''),
(31, 50, 3, '2024-05-07', 294.80, ''),
(32, 51, 3, '2024-05-10', 110.00, ''),
(33, 53, 1, '2024-05-23', 88.00, ''),
(34, 54, 3, '2024-06-08', 110.00, ''),
(35, 56, 3, '2024-06-17', 33.00, ''),
(36, 57, 1, '2024-06-18', 121.00, ''),
(37, 58, 3, '2024-06-20', 110.00, ''),
(38, 59, 3, '2024-07-10', 165.00, ''),
(39, 61, 3, '2024-07-30', 555.50, ''),
(40, 60, 3, '2024-08-10', 440.00, ''),
(41, 63, 3, '2024-08-16', 600.00, ''),
(42, 65, 3, '2024-09-12', 110.00, ''),
(43, 66, 1, '2024-09-13', 440.00, ''),
(44, 67, 1, '2024-09-14', 440.00, ''),
(45, 68, 1, '2024-09-20', 110.00, ''),
(46, 69, 1, '2024-09-30', 217.00, ''),
(47, 70, 1, '2024-11-19', 205.00, ''),
(48, 72, 1, '2024-12-13', 50.00, ''),
(49, 73, 3, '2025-01-21', 27.50, ''),
(50, 75, 3, '2025-02-12', 110.00, ''),
(51, 76, 1, '2025-02-22', 200.00, ''),
(52, 77, 3, '2025-03-20', 110.00, ''),
(53, 79, 1, '2025-05-05', 578.60, ''),
(54, 80, 3, '2025-06-15', 220.00, '');

-- --------------------------------------------------------

--
-- Table structure for table `ip_payment_custom`
--

CREATE TABLE `ip_payment_custom` (
  `payment_custom_id` int(11) NOT NULL,
  `payment_id` int(11) NOT NULL,
  `payment_custom_fieldid` int(11) NOT NULL,
  `payment_custom_fieldvalue` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `ip_payment_methods`
--

CREATE TABLE `ip_payment_methods` (
  `payment_method_id` int(11) NOT NULL,
  `payment_method_name` text DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `ip_payment_methods`
--

INSERT INTO `ip_payment_methods` (`payment_method_id`, `payment_method_name`) VALUES
(1, 'Cash'),
(2, 'Credit Card'),
(3, 'Bank transfer');

-- --------------------------------------------------------

--
-- Table structure for table `ip_products`
--

CREATE TABLE `ip_products` (
  `product_id` int(11) NOT NULL,
  `family_id` int(11) DEFAULT NULL,
  `product_sku` text DEFAULT NULL,
  `product_name` text DEFAULT NULL,
  `product_description` longtext NOT NULL,
  `product_price` decimal(20,2) DEFAULT NULL,
  `purchase_price` decimal(20,2) DEFAULT NULL,
  `provider_name` text DEFAULT NULL,
  `tax_rate_id` int(11) DEFAULT NULL,
  `unit_id` int(11) DEFAULT NULL,
  `product_tariff` int(11) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `ip_products`
--

INSERT INTO `ip_products` (`product_id`, `family_id`, `product_sku`, `product_name`, `product_description`, `product_price`, `purchase_price`, `provider_name`, `tax_rate_id`, `unit_id`, `product_tariff`) VALUES
(1, 1, '', 'PC service', '', 100.00, NULL, '', 2, NULL, 0),
(2, 2, '', 'Orico 2.5 Inch Hard Drive Adapter', 'Turns your 2.5 inch SATA HDD / SSD into 3.5 inch so you can install it into your desktop PC', 20.00, NULL, '', NULL, NULL, 0),
(3, 1, '', 'hours contract rate', '', 60.00, NULL, '', 2, NULL, 0),
(4, NULL, '', 'Kingston 1TB NV2 2280 NVMe SSD', '', 70.00, NULL, '', 2, NULL, 0),
(5, NULL, '', 'Silicon Power Ace A55 1TB TLC 3D NAND 2.5in SATA III SSD', '', 67.00, NULL, '', 2, NULL, 0),
(6, 2, '', 'Crucial MX500 2TB 3D NAND SATA 6Gbps 2.5in SSD 560MB/s 510MB/s', '', 179.00, NULL, '', 2, NULL, 0),
(7, NULL, '', 'Corsair 8GB (1x8GB) CMSO8GX3M1C1600C11 1600MHz Value Select DDR3L SODIMM RAM', '', 54.90, NULL, '', 2, NULL, 0),
(8, 3, '', 'Microsoft 365 Family 2021 English APAC 1 Year Subscription Medialess for PC & Mac', '', 110.00, NULL, '', 2, NULL, 0),
(9, 1, '', 'hours service home', '', 50.00, NULL, '', 2, NULL, 0),
(10, 4, '', 'Vision Australia Keyboard', '', 30.00, 30.00, 'Vision Australia', 2, NULL, 0),
(11, 2, '', 'Crucial BX500 2TB 3D NAND SATA 2.5in SSD', '', 145.00, 138.00, '', NULL, NULL, 0),
(12, 2, '', 'Corsair 550W CX550F RGB White 80+ Bronze Power Supply', '', 106.00, 104.00, '', NULL, NULL, 0),
(13, 2, '', 'Crucial MX500 1TB 3D 6Gbps 2.5in SSD 560MB/s 510MB/s NAND SATA SSD', '', 100.00, NULL, '', 2, NULL, 0),
(14, NULL, '', 'dvi to display port cable', '', 10.00, NULL, '', NULL, NULL, 0),
(15, NULL, '', 'Leader Corporate S44-i5 Slim Desktop, Intel i5-13400,16GB DDR5 RAM, 500GB M.2 NVMe SSD, 300W GOLD PSU, Win 11 Pro, 3 Years \"4 Hour\" Onsite Warranty', 'DESCRIPTION\r\n\r\nCPU\r\nIntel Core i5 13400 CPU 3.3GHz (4.6GHz Turbo) 13th Gen LGA1700 10-Cores 16-Threads 20MB 65W\r\n\r\nMainboard\r\nASUS Pro CSM Corporate Motherbaord B760M\r\n\r\nGraphics\r\nIntel UHD graphics 730\r\n\r\nMemory\r\nCrucial 16GB (1x16GB) DDR5 UDIMM 4800MHz CL40 Desktop PC Memory\r\n\r\nOptical\r\n24X DVD+/-R/RW DVD Burner with software.\r\n\r\nStorage\r\n500GB M.2 NVMe SSD\r\n\r\nCase\r\nLeader Intel Certified mATX slimline Silver/Black Thermal case. Advanced cooling and noise reduction features. Gold 80+ 300W PSU\r\n\r\nKeyboard\r\nWired Full Size Keyboard\r\n\r\nMouse\r\nWired Full Size Mouse\r\n\r\nOperating System\r\nWindows 11 Professional\r\n\r\nLAN\r\n1Gb Ethernet\r\n\r\nInputs/Outputs\r\n2x USB 3.2 Gen 1 ports (2 x Type-A)\r\n2x USB 2.0 ports (2 x Type-A)\r\n2x DisplayPorts\r\n1x HDMI® port\r\n1x VGA port\r\n1x Intel® 1Gb Ethernet port\r\n3x Audio jacks\r\n1x PS/2 keyboard (purple) port\r\n1x PS/2 mouse (green) port\r\n\r\nDimensions\r\n95x280x360mm (W/H/D)\r\n\r\nWarranty\r\n3 Years 4 Hour \"Leader Up and Running\" Australia Wide Onsite Warranty. 4 Hours is from time call logged during business hours Monday to Friday 9am - 5.30pm in metro areas only.\r\n', 1500.00, 1260.00, 'Leader Systems', 2, NULL, 0),
(16, 6, '', 'HP E24i G4 23.8\"/24\" WUXGA IPS Monitor Anti-Glare 1920x1200 DisplayPort VGA HDMI Tilt Swivel Pivot USB Hub 3yrs Wty', 'DESCRIPTION\r\n\r\nHP E24i G4 24\" WUXGA IPS 1920 x 1200 DisplayPort, VGA, HDMI, Tilt, Swivel, Pivot, USB, 3 YR WTY MONITOR (9VJ40AA)\r\n\r\nProduct specifications\r\n\r\nDisplay type IPS\r\n\r\nDisplay features Low blue light mode; Anti-glare\r\n\r\nOnscreen controls Brightness; Exit; Information; Management; Power control; Input control; Menu control; Image; Color\r\n\r\nNative resolution WUXGA (1920 x 1200)\r\n\r\nResolutions supported 1024 x 768; 1280 x 1024; 1280 x 720; 1280 x 800; 1440 x 900; 1600 x 900; 1680 x 1050; 1920 x 1080; 1920 x 1200; 640 x 480; 720 x 400; 800 x 600\r\n\r\nContrast ratio 1000:1\r\n\r\nBrightness 250 nits\r\n\r\nPixel pitch 0.27 mm\r\n\r\nSignal input connectors 1 VGA; 1 USB Type-B; 1 DisplayPort™ 1.2 (with HDCP support); 1 HDMI 1.4 (with HDCP support); 4 USB-A 3.2 Gen 1\r\n\r\nWebcam No integrated camera\r\n\r\nVESA Mounting 100 mm x 100 mm\r\n\r\nPower supply Input voltage 100 to 240 VAC\r\n\r\nDimensions (W X D X H) 20.94 x 1.85 x 13.88 in Without stand.\r\n\r\nWeight 13.36 lb\r\n\r\nWhat\'s in the box Monitor; DisplayPort™ 1.2 cable; HDMI cable; USB cable; QSP; AC power cable; Doc-kit\r\n', 360.00, 309.00, '', 2, NULL, 0),
(17, 3, '', 'M365 - Microsoft 365 Business Standard (New Commerce) 12 months subscription', '\r\n\r\nDesktop, web, and mobile versions of Word, Excel, PowerPoint, and Outlook\r\n\r\nCustom business email (you@yourbusiness.com)\r\n\r\nChat, call, collaborate, meet online, and host webinars up to 300 attendees\r\n\r\n1 TB of cloud storage per use\r\n\r\nVideo editing and design tools with Clipchamp\r\n', 224.40, 21.51, 'Microsoft through leader cloud', 2, NULL, 0),
(18, 7, '', 'MFC-L8390CDW *NEW*Compact Colour Laser Multi-Function Centre - Print/Scan/Copy/FAX with Print speeds of Up to 30 ppm, 2-Sided Printing & Scanning', 'DESCRIPTION\r\n\r\nBrother MFC-L8390CDW *NEW*Compact Colour Laser Multi-Function Centre - Print/Scan/Copy/FAX with Print speeds of Up to 30 ppm, 2-Sided Printing & Scanning, Wired & Wireless networking, ADF, 3.5” Touch Screen', 700.00, 550.20, 'Leader Systems', 2, NULL, 0),
(19, 4, '', 'Grandstream GUV3100 Full HD USB Webcam, 2 Built in Microphones, 1080p at 30fps, 1.8m USB Cable, Teams, Zoom, 3CX, 1 Meter Voice Pickup', 'The GUV3100 is a Full HD USB camera that enables high-quality audio and video collaboration through laptops, computers and more. This webcam supports 1080p Full HD real-time video through a 2 megapixel CMOS image sensor and includes 2 built-in omni-directional microphones with 1+ meter voice pickup range for clear communications. The GUV3100 is compatible with all major third-party communication platforms, apps and softphones as well as Grandstream’s IPVideoTalk Meetings and Wave app. Ideal for remote workers, the GUV3100 provides an easy-to-setup, easy-to-use USB webcam with Full HD video and audio quality for web meetings, video conferences and more.\r\n\r\n•Supports 1080p Full HD video at 30fps\r\n•USB 2.0 port offers plugand- play setup, no software download/installation needed\r\n•2 built-in microphones offer a 1+ meter voice pickup range\r\n•Compatible with all major third-party platforms, apps and softphones\r\n•Adjustable video settings include brightness, resolution, saturation, contrast, low-light and more', 40.00, 20.00, 'Leader Systems', 2, NULL, 0),
(20, 5, '', 'Leader Corporate S43 Slim Desktop, Intel i7-12700, 16GB RAM, 500GB M.2 NVMe SSD, 300W GOLD 80+ PSU, Windows 11 Pro, 3 Years \"4 Hour\" Onsite Warranty', '\r\nDESCRIPTION\r\n\r\nCPU\r\nIntel® 12th Generation Core i7-12700 12-Cores 20-Threads\r\n\r\nMainboard\r\nAsus Corporate Server grade \"Pro\" Intel B660M-C/CSM-S with 24/7 stability and reliability\r\n\r\nGraphics\r\nIntel HD graphics 730. Supports up to 3 displays simultaneously via 2x DP, 1x HDMI and 1x D-SUB\r\n\r\nMemory\r\n16GB (1x 16GB) DDR4 UDIMM RAM\r\n\r\nOptical\r\n24X DVD+/-R/RW DVD Burner with software\r\n\r\nStorage\r\n500GB M.2 NVMe SSD\r\n\r\nCase\r\nLeader mATX slimline Black Case. Advanced cooling and noise reduction features. Gold 80+ 300W PSU\r\n\r\nKeyboard & Mouse\r\nWired Full Size Keyboard and Mouse\r\n\r\nOperating System\r\nMicrosoft Windows 11 Professional\r\n\r\nEthernet\r\nGigabit LAN\r\n\r\nInputs/Outputs\r\n2x USB 3.2 Gen 1 ports (2 x Type-A), 2x USB 2.0 ports (2 x Type-A), 2x DisplayPort, 1x HDMI® port, 1x D-Sub port , 1x Intel® 1Gb Ethernet port , 3x Audio jacks, 1x PS/2 keyboard (purple) port , 1x PS/2 mouse (green) port\r\n\r\nDimensions\r\n95x280x360mm (W/H/D)\r\n\r\nWarranty\r\n3 Years 4 Hour \"Leader Up and Running\" Australia Wide Onsite Warranty. 4 Hours is from time call logged during business hours Monday to Friday 9am - 5.30pm in metro areas only.\r\n', 1600.00, 1364.00, 'Leader Systems', NULL, NULL, 0),
(21, 8, '', 'Simplecom CA315 1.5M USB 3.0 Extension Cable Gold Plated', 'USB extension cable', 10.00, 7.00, '', 2, NULL, 0),
(22, 9, 'SPLT-Z150', 'Logitech Z150 2.0 Stereo Speakers', 'Logitech Z150 2.0 Stereo Speakers 6W Compact Size Easily Access to Power & Volume Control Headphone & Auxiliary Jack for TV PC Smartphone Tablet', 45.00, 39.00, 'Leader Systems', 2, NULL, 0),
(23, 3, '', 'Macrium Reflect Workstation Annual Plan with Premium Support (3 Years)', 'Disk imaging and backup solution. 3 year license. Includes 3 years of product support through Macrium.', 300.00, 242.13, 'Macrium software', 2, NULL, 0),
(24, 10, '', 'Verbatim 2TB 2.5\" USB 3.0 Black Store\'n\'Go HDD Grid Design', 'External drive for computer backup. Large capacity of 2TB.', 130.00, 112.00, 'Leader Systems', 2, NULL, 0),
(25, 3, '', 'Reflect 8 Workstation with Premium Support (one time purchase)', '', 232.82, 182.26, 'Macrium software', 2, NULL, 0),
(26, 11, '', '24 Pin to 14 Pin PSU ATX Main Power Supply Adapter', 'adapter for proprietary Lenovo power supply', 4.00, NULL, '', 2, NULL, 0),
(27, 7, '', 'Epson Expression XP-6100 MFC Printer', 'Epson MFC printer', 159.00, 159.00, '', 2, NULL, 0),
(28, 2, '', 'Corsair  16GB (2x8GB) 3000Mhz DDR4 RAM', 'Corsair Vengeance LPX 16GB (2x8GB) 3000Mhz DDR4 RAM', 68.00, NULL, '', NULL, NULL, 0),
(29, 1, '', 'half hour remote IT support', '', 30.00, NULL, '', 2, NULL, 0),
(30, 2, '', 'Silicon Power Ace A55 256GB TLC 3D NAND 2.5in SATA III SSD', '', 40.00, NULL, '', 2, NULL, 0),
(31, 12, '', 'Crucial P3 PCIe Gen3 NVMe M.2 SSD - 500GB', 'Faster storage device NVMe', 65.00, 65.00, 'PLE', 2, NULL, 0),
(32, NULL, '', 'TP-LINK 8-port Desktop Gigabit Switch', '8 10/100/1000M RJ45 ports, plastic case (TL-SG1008D)', 35.00, 33.00, 'Umart', 2, NULL, 0),
(33, 8, '', 'DVI-D Dual Link M-M Cable', 'DVI cable', 5.00, NULL, '', 2, NULL, 0),
(34, 13, '', 'TP-Link AC2100 Wireless Modem Router', 'TP-Link AC2100 Wireless MU-MIMO Modem Router', 225.00, NULL, 'Umart', 2, NULL, 0),
(35, 9, '', 'Creative Stage SE Mini Speakers Sound Bar ', 'Creative Stage SE Mini Speakers Sound Bar ', 80.00, NULL, 'Umart', 2, NULL, 0),
(36, 5, '', 'EO 870 G9 R NT I7-13700 16GB 512GB VPRO', 'HP ELITEONE 870 G9 R ALL-IN-ONE 27 INCH FHD NON TOUCH SCREEN i7-13700 VPRO 16GB DDR5-4800 512GB PCIE SSD 5MP WEBCAM WIFI-6 BT-5.3 SDC-READER SPK WL KB MOUSE Windows 11 Pro 3/3/3 WARRANTY', 2250.00, NULL, 'Ingram Micro', 2, NULL, 0),
(37, 1, '', 'half hour remote IT support A1', '', 50.00, NULL, '', 2, NULL, 0),
(38, 1, '', 'hour IT support A1', '', 200.00, NULL, '', 2, NULL, 0),
(39, 5, '', 'Leader Visionary AIO, 27\" FHD, Intel i5-12450H', 'Leader Visionary AIO, 27\" FHD, Intel i5-12450H, 16GB DDR4, 1TB NVMe SSD, Wi-Fi 6, 2M Camera, VESA, 1 Year Warranty, Windows 11 Home, Keyboard & Mouse', 1400.00, NULL, '', 2, NULL, 0),
(40, 2, '', 'Thermaltake 650W Smart Pro RGB', 'Thermaltake 650W Smart Pro RGB Bronze Fully Modular Power Supply', 100.00, NULL, '', 2, NULL, 0),
(41, 12, '', 'Kingston NV2 500GB NVMe SSD', 'Kingston NV2 500GB PCIe 4.0 M.2 2280 NVMe SSD', 55.00, NULL, '', NULL, NULL, 0),
(42, 2, '', '16 GB DDR4 SO-DIMM', '', 50.00, NULL, '', NULL, NULL, 0),
(43, 14, '', 'Lenovo Tab M11 WiFi', 'tablet for e-mail', 300.00, NULL, '', 2, NULL, 0),
(44, 2, '', 'MSI B550-A PRO AM4 ATX Motherboard (B550-A PRO)', 'MSI motherboard for system upgrade to support Windows 11', 166.00, NULL, '', 2, NULL, 0),
(45, 2, '', 'Corsair 16GB (2x8GB) 2666Mhz DDR4 RAM', 'DDR RAM for new motherboard', 60.00, NULL, '', 2, NULL, 0),
(46, 15, '', 'MSI Cubi NUC 5 12M-201BAU Mini PC barebone', 'MSI Cubi NUC 5 12M-201BAU Mini PC barebone Intel i5-1235U 2xDDR4 upto 64GB, Intel® Iris® Xe Graphics 1x M.2,1x2.5\"SSD, (similar to RNUC12WSHI50001)', 500.00, NULL, '', 2, NULL, 0),
(47, 3, '', 'Microsoft Windows 11 Professional ', 'Microsoft Windows 11 Professional OEM 64-bit English 1 Pack DVD. Key NEW', 247.00, NULL, '', 2, NULL, 0),
(48, 6, '', 'ViewSonic 32” VA3209U-4K 4K ', 'ViewSonic 32” VA3209U-4K 4K Business, Seamless Viewing, USB-C, DP, HDMI x 2, Speakers, Eco Mode VESA 100x100 Business and Office Monitor (LS)', 600.00, NULL, '', 2, NULL, 0),
(49, 16, '', 'Crucial 8GB (1x8GB) DDR4 SODIMM ', 'Crucial 8GB (1x8GB) DDR4 SODIMM 3200MHz CL22 1.2V Single Ranked Notebook Laptop Memory RAM ~CT8G4SFRA32A', 55.00, NULL, '', 2, NULL, 0),
(50, 12, '', 'Crucial P3 2TB Gen3 NVMe SSD', 'Crucial P3 2TB Gen3 NVMe SSD 3500/3000 MB/s R/W 440TBW 650K/700K IOPS 1.5M hrs MTTF Full-Drive Encryption M.2 PCIe3 5yrs ~CT2000P3PSSD8', 186.00, NULL, '', 2, NULL, 0);

-- --------------------------------------------------------

--
-- Table structure for table `ip_projects`
--

CREATE TABLE `ip_projects` (
  `project_id` int(11) NOT NULL,
  `client_id` int(11) NOT NULL,
  `project_name` text DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `ip_projects`
--

INSERT INTO `ip_projects` (`project_id`, `client_id`, `project_name`) VALUES
(1, 4, 'test');

-- --------------------------------------------------------

--
-- Table structure for table `ip_quotes`
--

CREATE TABLE `ip_quotes` (
  `quote_id` int(11) NOT NULL,
  `invoice_id` int(11) NOT NULL DEFAULT 0,
  `user_id` int(11) NOT NULL,
  `client_id` int(11) NOT NULL,
  `invoice_group_id` int(11) NOT NULL,
  `quote_status_id` tinyint(2) NOT NULL DEFAULT 1,
  `quote_date_created` date NOT NULL,
  `quote_date_modified` datetime NOT NULL,
  `quote_date_expires` date NOT NULL,
  `quote_number` varchar(100) DEFAULT NULL,
  `quote_discount_amount` decimal(20,2) DEFAULT NULL,
  `quote_discount_percent` decimal(20,2) DEFAULT NULL,
  `quote_url_key` char(32) NOT NULL,
  `quote_password` varchar(90) DEFAULT NULL,
  `notes` longtext DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `ip_quotes`
--

INSERT INTO `ip_quotes` (`quote_id`, `invoice_id`, `user_id`, `client_id`, `invoice_group_id`, `quote_status_id`, `quote_date_created`, `quote_date_modified`, `quote_date_expires`, `quote_number`, `quote_discount_amount`, `quote_discount_percent`, `quote_url_key`, `quote_password`, `notes`) VALUES
(2, 3, 1, 1, 4, 4, '2022-12-13', '2022-12-13 09:56:21', '2022-12-28', 'QUO2', 0.00, 0.00, 'XqOpM3tiougJT6v2C8EnD7LIwBklzaSf', '', ''),
(4, 13, 1, 4, 4, 4, '2023-04-30', '2023-04-30 10:29:06', '2023-05-16', 'QUO4', 0.00, 0.00, '7lYLg5dh8ByqPmobzKWFSNMTut4Xfpr2', '', ''),
(5, 21, 1, 10, 4, 4, '2023-06-20', '2023-06-21 05:12:30', '2023-07-06', 'QUO5', 0.00, 0.00, 'Jmf0EY6bLH9A3Sluv7GzOUc5gDXsVp1a', '', ''),
(6, 33, 1, 22, 4, 4, '2024-02-15', '2024-02-15 05:08:46', '2024-03-02', 'QUO6', 0.00, 0.00, 'b8LfKRc0WV65Yn9AjwtsB2hNl3IG1aqy', '', ''),
(7, 0, 1, 22, 4, 2, '2024-02-29', '2024-02-29 01:37:00', '2024-03-16', 'QUO7', 0.00, 0.00, 'L4JhalZkfTeSYdDsAQ9VmFRWwMq5XpCo', '', ''),
(10, 44, 1, 24, 4, 2, '2024-02-29', '2024-02-29 06:01:28', '2024-03-16', 'QUO9', 0.00, 0.00, 'P3TNGFlChIYu8JwsRX1kyQinOUvSdEKM', '', ''),
(9, 39, 1, 22, 4, 4, '2024-02-29', '2024-03-05 02:56:34', '2024-03-16', 'QUO8', 0.00, 0.00, 'f04r6mR8LVCbOaYKAHiSq95PyvNM2T37', '', ''),
(11, 0, 1, 37, 4, 3, '2024-08-26', '2024-08-26 09:48:23', '2024-09-11', 'QUO10', 0.00, 0.00, 'WOvXLIh0A6ScfHDPuQNgrEzUkjpYJ1tn', '', ''),
(12, 0, 1, 37, 4, 3, '2024-08-26', '2024-09-10 03:41:02', '2024-09-11', 'QUO11', 0.00, 0.00, 'ioRyBxhb28IkMp4PKF7vaqYrZHUzC1ul', '', ''),
(13, 0, 1, 38, 4, 1, '2024-09-13', '2024-09-13 06:23:08', '2024-09-29', '', NULL, NULL, 'lP85uhro3SkGyxMFbWXTNwA7IEvf4UtV', '', ''),
(14, 0, 1, 36, 4, 1, '2025-07-07', '2025-07-07 23:46:47', '2025-07-23', '', NULL, NULL, 'avkSBwEbxCc30mNiUVLjZOfuQ8G1AJD6', '', ''),
(15, 0, 1, 25, 4, 1, '2025-07-09', '2025-07-09 04:06:23', '2025-07-25', '', NULL, NULL, 'PqTdAuYQRH0ZIvBFXtUpSG6LC7OJ49rg', '', ''),
(16, 0, 1, 25, 4, 4, '2025-07-09', '2025-07-09 09:20:41', '2025-07-25', 'QUO12', 0.00, 0.00, 'xFjtcqHEdMhBeO2lsmN5PGyoKfI0S14C', '', ''),
(17, 0, 1, 25, 4, 2, '2025-07-09', '2025-07-09 10:50:45', '2025-07-25', 'QUO13', 0.00, 0.00, 'RA9GFfti5yT2OwpbUaqEJ3nl80BSsVzQ', '', ''),
(18, 0, 1, 25, 4, 1, '2025-07-18', '2025-07-18 14:53:26', '2025-08-03', '', NULL, NULL, 'tNLix1Zc8DrEIuf5ygbT4OR7FVH0wphd', '', ''),
(19, 0, 1, 25, 4, 1, '2025-07-23', '2025-07-23 05:56:37', '2025-08-08', '', NULL, NULL, '2MNxsZarSGAPw4OC83fqJmUgbui6tWpn', '', ''),
(20, 0, 1, 45, 4, 3, '2025-07-31', '2025-08-01 01:14:11', '2025-08-16', 'QUO14', 0.00, 0.00, 'BYRmeiZz23w8kKW5NcdtrHFT0vA4SMnP', '', '');

-- --------------------------------------------------------

--
-- Table structure for table `ip_quote_amounts`
--

CREATE TABLE `ip_quote_amounts` (
  `quote_amount_id` int(11) NOT NULL,
  `quote_id` int(11) NOT NULL,
  `quote_item_subtotal` decimal(20,2) DEFAULT NULL,
  `quote_item_tax_total` decimal(20,2) DEFAULT NULL,
  `quote_tax_total` decimal(20,2) DEFAULT NULL,
  `quote_total` decimal(20,2) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `ip_quote_amounts`
--

INSERT INTO `ip_quote_amounts` (`quote_amount_id`, `quote_id`, `quote_item_subtotal`, `quote_item_tax_total`, `quote_tax_total`, `quote_total`) VALUES
(2, 2, 45.00, 0.00, 0.00, 45.00),
(4, 4, 200.00, 20.00, 0.00, 220.00),
(5, 5, 167.00, 16.70, 0.00, 183.70),
(6, 6, 5984.80, 598.48, 0.00, 6583.28),
(7, 7, 530.00, 53.00, 0.00, 583.00),
(10, 10, 204.00, 20.40, 0.00, 224.40),
(9, 9, 462.82, 46.28, 0.00, 509.10),
(11, 11, 2450.00, 245.00, 0.00, 2695.00),
(12, 12, 1600.00, 160.00, 0.00, 1760.00),
(13, 13, NULL, NULL, NULL, NULL),
(14, 14, NULL, NULL, NULL, NULL),
(15, 15, NULL, NULL, NULL, NULL),
(16, 16, 10.00, 0.00, 0.00, 10.00),
(17, 17, 0.00, NULL, 0.00, 0.00),
(18, 18, NULL, NULL, NULL, NULL),
(19, 19, NULL, NULL, NULL, NULL),
(20, 20, 2143.00, 214.30, 0.00, 2357.30);

-- --------------------------------------------------------

--
-- Table structure for table `ip_quote_custom`
--

CREATE TABLE `ip_quote_custom` (
  `quote_custom_id` int(11) NOT NULL,
  `quote_id` int(11) NOT NULL,
  `quote_custom_fieldid` int(11) NOT NULL,
  `quote_custom_fieldvalue` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `ip_quote_items`
--

CREATE TABLE `ip_quote_items` (
  `item_id` int(11) NOT NULL,
  `quote_id` int(11) NOT NULL,
  `item_tax_rate_id` int(11) NOT NULL,
  `item_product_id` int(11) DEFAULT NULL,
  `item_date_added` date NOT NULL,
  `item_name` text DEFAULT NULL,
  `item_description` text DEFAULT NULL,
  `item_quantity` decimal(20,2) DEFAULT NULL,
  `item_price` decimal(20,2) DEFAULT NULL,
  `item_discount_amount` decimal(20,2) DEFAULT NULL,
  `item_order` int(2) NOT NULL DEFAULT 0,
  `item_product_unit` varchar(50) DEFAULT NULL,
  `item_product_unit_id` int(11) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `ip_quote_items`
--

INSERT INTO `ip_quote_items` (`item_id`, `quote_id`, `item_tax_rate_id`, `item_product_id`, `item_date_added`, `item_name`, `item_description`, `item_quantity`, `item_price`, `item_discount_amount`, `item_order`, `item_product_unit`, `item_product_unit_id`) VALUES
(4, 2, 0, 1, '2022-12-13', 'PC service', '', 0.25, 100.00, NULL, 2, NULL, NULL),
(3, 2, 0, 2, '2022-12-13', 'Orico 2.5 Inch Hard Drive Adapter', 'Turns your 2.5 inch SATA HDD / SSD into 3.5 inch so you can install it into your desktop PC', 1.00, 20.00, NULL, 1, NULL, NULL),
(5, 4, 2, 1, '2023-04-30', 'PC service', 'run diagnostics on HP Pavilion desktop\ncreate backup image\ninstall HP recovery image\nrecover files from backup image\n', 2.00, 100.00, NULL, 1, NULL, NULL),
(6, 5, 2, 5, '2023-06-20', 'Silicon Power Ace A55 1TB TLC 3D NAND 2.5in SATA III SSD', 'New SSD drive to increase the speed and storage capacity of your Toshiba laptop.', 1.00, 67.00, NULL, 1, NULL, NULL),
(7, 5, 2, 9, '2023-06-20', 'hours service home', 'open up Toshiba Satellite Pro L50-A case and remove HDD.\nClone HDD to SSD drive.\nInstall new SSD drive and close Toshiba case. ', 2.00, 50.00, NULL, 2, NULL, NULL),
(15, 6, 2, 20, '2024-02-15', 'Leader Corporate S43 Slim Desktop, Intel i7-12700, 16GB RAM, 500GB M.2 NVMe SSD, 300W GOLD 80+ PSU, Windows 11 Pro, 3 Years \"4 Hour\" Onsite Warranty', 'DESCRIPTION\n\nCPU\nIntel® 12th Generation Core i7-12700 12-Cores 20-Threads\n\nMainboard\nAsus Corporate Server grade \"Pro\" Intel B660M-C/CSM-S with 24/7 stability and reliability\n\nGraphics\nIntel HD graphics 730. Supports up to 3 displays simultaneously via 2x DP, 1x HDMI and 1x D-SUB\n\nMemory\n16GB (1x 16GB) DDR4 UDIMM RAM\n\nOptical\n24X DVD+/-R/RW DVD Burner with software\n\nStorage\n500GB M.2 NVMe SSD\n\nCase\nLeader mATX slimline Black Case. Advanced cooling and noise reduction features. Gold 80+ 300W PSU\n\nKeyboard & Mouse\nWired Full Size Keyboard and Mouse\n\nOperating System\nMicrosoft Windows 11 Professional\n\nEthernet\nGigabit LAN\n\nInputs/Outputs\n2x USB 3.2 Gen 1 ports (2 x Type-A), 2x USB 2.0 ports (2 x Type-A), 2x DisplayPort, 1x HDMI® port, 1x D-Sub port , 1x Intel® 1Gb Ethernet port , 3x Audio jacks, 1x PS/2 keyboard (purple) port , 1x PS/2 mouse (green) port\n\nDimensions\n95x280x360mm (W/H/D)\n\nWarranty\n3 Years 4 Hour \"Leader Up and Running\" Australia Wide Onsite Warranty. 4 Hours is from time call logged during business hours Monday to Friday 9am - 5.30pm in metro areas only.\n', 2.00, 1600.00, NULL, 1, NULL, NULL),
(10, 6, 2, 16, '2024-02-15', 'HP E24i G4 23.8\"/24\" WUXGA IPS Monitor Anti-Glare 1920x1200 DisplayPort VGA HDMI Tilt Swivel Pivot USB Hub 3yrs Wty', 'DESCRIPTION\n\nHP E24i G4 24\" WUXGA IPS 1920 x 1200 DisplayPort, VGA, HDMI, Tilt, Swivel, Pivot, USB, 3 YR WTY MONITOR (9VJ40AA)\n\nProduct specifications\n\nDisplay type IPS\n\nDisplay features Low blue light mode; Anti-glare\n\nOnscreen controls Brightness; Exit; Information; Management; Power control; Input control; Menu control; Image; Color\n\nNative resolution WUXGA (1920 x 1200)\n\nResolutions supported 1024 x 768; 1280 x 1024; 1280 x 720; 1280 x 800; 1440 x 900; 1600 x 900; 1680 x 1050; 1920 x 1080; 1920 x 1200; 640 x 480; 720 x 400; 800 x 600\n\nContrast ratio 1000:1\n\nBrightness 250 nits\n\nPixel pitch 0.27 mm\n\nSignal input connectors 1 VGA; 1 USB Type-B; 1 DisplayPort™ 1.2 (with HDCP support); 1 HDMI 1.4 (with HDCP support); 4 USB-A 3.2 Gen 1\n\nWebcam No integrated camera\n\nVESA Mounting 100 mm x 100 mm\n\nPower supply Input voltage 100 to 240 VAC\n\nDimensions (W X D X H) 20.94 x 1.85 x 13.88 in Without stand.\n\nWeight 13.36 lb\n\nWhat\'s in the box Monitor; DisplayPort™ 1.2 cable; HDMI cable; USB cable; QSP; AC power cable; Doc-kit\n', 4.00, 309.00, NULL, 2, NULL, NULL),
(11, 6, 2, 17, '2024-02-15', 'M365 - Microsoft 365 Business Standard (New Commerce) 12 months subscription', 'Desktop, web, and mobile versions of Word, Excel, PowerPoint, and Outlook\n\nCustom business email (you@yourbusiness.com)\n\nChat, call, collaborate, meet online, and host webinars up to 300 attendees\n\n1 TB of cloud storage per use\n\nVideo editing and design tools with Clipchamp\n', 2.00, 224.40, NULL, 3, NULL, NULL),
(12, 6, 2, 18, '2024-02-15', 'MFC-L8390CDW *NEW*Compact Colour Laser Multi-Function Centre - Print/Scan/Copy/FAX with Print speeds of Up to 30 ppm, 2-Sided Printing & Scanning', 'DESCRIPTION\n\nBrother MFC-L8390CDW *NEW*Compact Colour Laser Multi-Function Centre - Print/Scan/Copy/FAX with Print speeds of Up to 30 ppm, 2-Sided Printing & Scanning, Wired & Wireless networking, ADF, 3.5” Touch Screen', 1.00, 700.00, NULL, 4, NULL, NULL),
(13, 6, 2, 1, '2024-02-15', 'PC service', 'Setup new computers and printer, migrate data, setup office and e-mail', 4.00, 100.00, NULL, 5, NULL, NULL),
(16, 7, 2, 23, '2024-02-29', 'Macrium Reflect Workstation Annual Plan with Premium Support (3 Years)', 'Disk imaging and backup solution. 3 year license. Includes 3 years of product support through Macrium.', 1.00, 300.00, NULL, 1, NULL, NULL),
(17, 7, 2, 24, '2024-02-29', 'Verbatim 2TB 2.5\" USB 3.0 Black Store\'n\'Go HDD Grid Design', 'External drive for computer backup. Large capacity of 2TB.', 1.00, 130.00, NULL, 2, NULL, NULL),
(18, 7, 2, 1, '2024-02-29', 'PC service', 'Onsite setup to activate software license and install backup drive. ', 1.00, 100.00, NULL, 3, NULL, NULL),
(27, 10, 2, 9, '2024-02-29', 'hours service home', 'Install replacement PSU (power supply unit) and adapter as well as new solid state drive. Transfer data accross.', 2.00, 50.00, NULL, 3, NULL, NULL),
(26, 10, 2, 26, '2024-02-29', '24 Pin to 14 Pin PSU ATX Main Power Supply Adapter', 'adapter for proprietary Lenovo power supply', 1.00, 4.00, NULL, 2, NULL, NULL),
(25, 10, 2, 13, '2024-02-29', 'Crucial MX500 1TB 3D 6Gbps 2.5in SSD 560MB/s 510MB/s NAND SATA SSD', 'new Solid state drive (C drive)', 1.00, 100.00, NULL, 1, NULL, NULL),
(22, 9, 2, 25, '2024-02-29', 'Reflect 8 Workstation with Premium Support (one time purchase)', 'Macrium Reflect backup software one time purchase. Product support is limited to the first year unless renewed.', 1.00, 232.82, NULL, 1, NULL, NULL),
(23, 9, 2, 24, '2024-02-29', 'Verbatim 2TB 2.5\" USB 3.0 Black Store\'n\'Go HDD Grid Design', 'External drive for computer backup. Large capacity of 2TB.', 1.00, 130.00, NULL, 2, NULL, NULL),
(24, 9, 2, 1, '2024-02-29', 'PC service', 'Onsite setup to activate software license\n\nand install backup drive.', 1.00, 100.00, NULL, 3, NULL, NULL),
(28, 11, 2, 36, '2024-08-26', 'EO 870 G9 R NT I7-13700 16GB 512GB VPRO', 'HP ELITEONE 870 G9 R ALL-IN-ONE 27 INCH FHD NON TOUCH SCREEN i7-13700 VPRO 16GB DDR5-4800 512GB PCIE SSD 5MP WEBCAM WIFI-6 BT-5.3 SDC-READER SPK WL KB MOUSE Windows 11 Pro 3/3/3 WARRANTY', 1.00, 2250.00, NULL, 1, NULL, NULL),
(29, 11, 2, 1, '2024-08-26', 'PC service', 'setup of new HP AIO PC', 2.00, 100.00, NULL, 2, NULL, NULL),
(30, 12, 2, 39, '2024-09-10', 'Leader Visionary AIO, 27\" FHD, Intel i5-12450H', 'Leader Visionary AIO, 27\" FHD, Intel i5-12450H, 16GB DDR4, 1TB NVMe SSD, Wi-Fi 6, 2M Camera, VESA, 1 Year Warranty, Windows 11 Home, Keyboard & Mouse', 1.00, 1400.00, NULL, 1, NULL, NULL),
(31, 12, 2, 1, '2024-09-10', 'PC service', '2 hours setup', 2.00, 100.00, NULL, 2, NULL, NULL),
(32, 16, 0, 14, '2025-07-09', 'dvi to display port cable', '', 1.00, 10.00, NULL, 1, NULL, NULL),
(33, 20, 2, NULL, '2025-07-31', 'Crucial 8GB (1x8GB) DDR4 SODIMM ', 'Crucial 8GB (1x8GB) DDR4 SODIMM 3200MHz CL22 1.2V Single Ranked Notebook Laptop Memory RAM ~CT8G4SFRA32A', 2.00, 55.00, NULL, 1, NULL, NULL),
(34, 20, 2, 46, '2025-08-01', 'MSI Cubi NUC 5 12M-201BAU Mini PC barebone', 'MSI Cubi NUC 5 12M-201BAU Mini PC barebone Intel i5-1235U 2xDDR4 upto 64GB, Intel® Iris® Xe Graphics 1x M.2,1x2.5\"SSD, (similar to RNUC12WSHI50001)', 1.00, 500.00, NULL, 2, NULL, NULL),
(35, 20, 2, 48, '2025-08-01', 'ViewSonic 32” VA3209U-4K 4K ', 'ViewSonic 32” VA3209U-4K 4K Business, Seamless Viewing, USB-C, DP, HDMI x 2, Speakers, Eco Mode VESA 100x100 Business and Office Monitor (LS)', 1.00, 600.00, NULL, 3, NULL, NULL),
(37, 20, 2, 47, '2025-08-01', 'Microsoft Windows 11 Professional ', 'Microsoft Windows 11 Professional OEM 64-bit English 1 Pack DVD. Key NEW', 1.00, 247.00, NULL, 4, NULL, NULL),
(38, 20, 2, 50, '2025-08-01', 'Crucial P3 2TB Gen3 NVMe SSD', 'Crucial P3 2TB Gen3 NVMe SSD 3500/3000 MB/s R/W 440TBW 650K/700K IOPS 1.5M hrs MTTF Full-Drive Encryption M.2 PCIe3 5yrs ~CT2000P3PSSD8', 1.00, 186.00, NULL, 5, NULL, NULL),
(39, 20, 2, 1, '2025-08-01', 'PC service', '5 hours setup, install, configuration, service, support', 5.00, 100.00, NULL, 6, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `ip_quote_item_amounts`
--

CREATE TABLE `ip_quote_item_amounts` (
  `item_amount_id` int(11) NOT NULL,
  `item_id` int(11) NOT NULL,
  `item_subtotal` decimal(20,2) DEFAULT NULL,
  `item_tax_total` decimal(20,2) DEFAULT NULL,
  `item_discount` decimal(20,2) DEFAULT NULL,
  `item_total` decimal(20,2) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `ip_quote_item_amounts`
--

INSERT INTO `ip_quote_item_amounts` (`item_amount_id`, `item_id`, `item_subtotal`, `item_tax_total`, `item_discount`, `item_total`) VALUES
(4, 4, 25.00, 0.00, 0.00, 25.00),
(3, 3, 20.00, 0.00, 0.00, 20.00),
(5, 5, 200.00, 20.00, 0.00, 220.00),
(6, 6, 67.00, 6.70, 0.00, 73.70),
(7, 7, 100.00, 10.00, 0.00, 110.00),
(15, 15, 3200.00, 320.00, 0.00, 3520.00),
(16, 16, 300.00, 30.00, 0.00, 330.00),
(10, 10, 1236.00, 123.60, 0.00, 1359.60),
(11, 11, 448.80, 44.88, 0.00, 493.68),
(12, 12, 700.00, 70.00, 0.00, 770.00),
(13, 13, 400.00, 40.00, 0.00, 440.00),
(17, 17, 130.00, 13.00, 0.00, 143.00),
(18, 18, 100.00, 10.00, 0.00, 110.00),
(27, 27, 100.00, 10.00, 0.00, 110.00),
(26, 26, 4.00, 0.40, 0.00, 4.40),
(25, 25, 100.00, 10.00, 0.00, 110.00),
(22, 22, 232.82, 23.28, 0.00, 256.10),
(23, 23, 130.00, 13.00, 0.00, 143.00),
(24, 24, 100.00, 10.00, 0.00, 110.00),
(28, 28, 2250.00, 225.00, 0.00, 2475.00),
(29, 29, 200.00, 20.00, 0.00, 220.00),
(30, 30, 1400.00, 140.00, 0.00, 1540.00),
(31, 31, 200.00, 20.00, 0.00, 220.00),
(32, 32, 10.00, 0.00, 0.00, 10.00),
(33, 33, 110.00, 11.00, 0.00, 121.00),
(34, 34, 500.00, 50.00, 0.00, 550.00),
(35, 35, 600.00, 60.00, 0.00, 660.00),
(37, 37, 247.00, 24.70, 0.00, 271.70),
(38, 38, 186.00, 18.60, 0.00, 204.60),
(39, 39, 500.00, 50.00, 0.00, 550.00);

-- --------------------------------------------------------

--
-- Table structure for table `ip_quote_tax_rates`
--

CREATE TABLE `ip_quote_tax_rates` (
  `quote_tax_rate_id` int(11) NOT NULL,
  `quote_id` int(11) NOT NULL,
  `tax_rate_id` int(11) NOT NULL,
  `include_item_tax` int(1) NOT NULL DEFAULT 0,
  `quote_tax_rate_amount` decimal(20,2) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `ip_sessions`
--

CREATE TABLE `ip_sessions` (
  `id` varchar(128) NOT NULL,
  `ip_address` varchar(45) NOT NULL,
  `timestamp` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `data` blob NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `ip_settings`
--

CREATE TABLE `ip_settings` (
  `setting_id` int(11) NOT NULL,
  `setting_key` varchar(50) NOT NULL,
  `setting_value` longtext NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `ip_settings`
--

INSERT INTO `ip_settings` (`setting_id`, `setting_key`, `setting_value`) VALUES
(19, 'default_language', 'english'),
(20, 'date_format', 'd/m/Y'),
(21, 'currency_symbol', '$'),
(22, 'currency_symbol_placement', 'before'),
(23, 'currency_code', 'AUD'),
(24, 'invoices_due_after', '14'),
(25, 'quotes_expire_after', '16'),
(26, 'default_invoice_group', '3'),
(27, 'default_quote_group', '4'),
(28, 'thousands_separator', ','),
(29, 'decimal_point', '.'),
(30, 'cron_key', 'GUdxeh4Cvw7ELXy6'),
(31, 'tax_rate_decimal_places', '2'),
(32, 'pdf_invoice_template', 'InvoicePlaneGST'),
(33, 'pdf_invoice_template_paid', 'InvoicePlaneGSTpaid'),
(34, 'pdf_invoice_template_overdue', 'InvoicePlane - overdue'),
(35, 'pdf_quote_template', 'InvoicePlaneGST'),
(36, 'public_invoice_template', 'InvoicePlane_Web'),
(37, 'public_quote_template', 'InvoicePlane_Web'),
(38, 'disable_sidebar', '1'),
(39, 'read_only_toggle', '4'),
(40, 'invoice_pre_password', ''),
(41, 'quote_pre_password', ''),
(42, 'email_pdf_attachment', '1'),
(43, 'generate_invoice_number_for_draft', '0'),
(44, 'generate_quote_number_for_draft', '0'),
(45, 'sumex', '0'),
(46, 'sumex_sliptype', '1'),
(47, 'sumex_canton', '0'),
(48, 'system_theme', 'invoiceplane'),
(49, 'default_hourly_rate', '0.00'),
(50, 'projects_enabled', '1'),
(51, 'pdf_quote_footer', ''),
(52, 'enable_permissive_search_clients', '1'),
(53, 'first_day_of_week', '0'),
(54, 'default_country', 'AU'),
(55, 'default_list_limit', '15'),
(56, 'number_format', 'number_format_us_uk'),
(57, 'quote_overview_period', 'this-month'),
(58, 'invoice_overview_period', 'this-month'),
(59, 'disable_quickactions', '0'),
(60, 'custom_title', ''),
(61, 'monospace_amounts', '0'),
(62, 'reports_in_new_tab', '0'),
(63, 'show_responsive_itemlist', '0'),
(64, 'bcc_mails_to_admin', '0'),
(65, 'default_invoice_terms', 'Please pay within 14 days.\r\nMake payment to:\r\nTYPE1CIV Pty Ltd\r\n\r\nBANK NAME: ANZ - Airwallex Pty Ltd\r\nAccount: 612082265\r\nBSB: 013943\r\n\r\nPlease quote the invoice number in the payment reference.'),
(66, 'invoice_default_payment_method', ''),
(67, 'mark_invoices_sent_pdf', '0'),
(68, 'include_zugferd', '0'),
(69, 'pdf_watermark', '0'),
(70, 'email_invoice_template', ''),
(71, 'email_invoice_template_paid', ''),
(72, 'email_invoice_template_overdue', ''),
(73, 'pdf_invoice_footer', 'On behalf of the team at Aptitude Technology we thank you for your business.\r\nE-mail: support@aptitudetech.com.au\r\nPh: (08) 9386 0020\r\nmobile: 0404 978 533'),
(74, 'automatic_email_on_recur', '0'),
(75, 'sumex_role', '0'),
(76, 'sumex_place', '0'),
(77, 'default_quote_notes', ''),
(78, 'mark_quotes_sent_pdf', '0'),
(79, 'email_quote_template', ''),
(80, 'default_invoice_tax_rate', ''),
(81, 'default_item_tax_rate', ''),
(82, 'default_include_item_tax', ''),
(83, 'email_send_method', ''),
(84, 'smtp_server_address', ''),
(85, 'smtp_mail_from', ''),
(86, 'smtp_authentication', '0'),
(87, 'smtp_username', ''),
(88, 'smtp_port', ''),
(89, 'smtp_security', ''),
(90, 'smtp_verify_certs', '1'),
(91, 'enable_online_payments', '0'),
(92, 'gateway_stripe_enabled', '0'),
(93, 'gateway_stripe_apiKeyPublic', ''),
(94, 'gateway_stripe_currency', 'AFN'),
(95, 'gateway_stripe_payment_method', '');

-- --------------------------------------------------------

--
-- Table structure for table `ip_tasks`
--

CREATE TABLE `ip_tasks` (
  `task_id` int(11) NOT NULL,
  `project_id` int(11) NOT NULL,
  `task_name` text DEFAULT NULL,
  `task_description` longtext NOT NULL,
  `task_price` decimal(20,2) DEFAULT NULL,
  `task_finish_date` date NOT NULL,
  `task_status` tinyint(1) NOT NULL,
  `tax_rate_id` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `ip_tax_rates`
--

CREATE TABLE `ip_tax_rates` (
  `tax_rate_id` int(11) NOT NULL,
  `tax_rate_name` text DEFAULT NULL,
  `tax_rate_percent` decimal(5,2) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `ip_tax_rates`
--

INSERT INTO `ip_tax_rates` (`tax_rate_id`, `tax_rate_name`, `tax_rate_percent`) VALUES
(2, 'gst', 10.00);

-- --------------------------------------------------------

--
-- Table structure for table `ip_units`
--

CREATE TABLE `ip_units` (
  `unit_id` int(11) NOT NULL,
  `unit_name` varchar(50) DEFAULT NULL,
  `unit_name_plrl` varchar(50) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `ip_uploads`
--

CREATE TABLE `ip_uploads` (
  `upload_id` int(11) NOT NULL,
  `client_id` int(11) NOT NULL,
  `url_key` char(32) NOT NULL,
  `file_name_original` longtext NOT NULL,
  `file_name_new` longtext NOT NULL,
  `uploaded_date` date NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `ip_users`
--

CREATE TABLE `ip_users` (
  `user_id` int(11) NOT NULL,
  `user_type` int(1) NOT NULL DEFAULT 0,
  `user_active` tinyint(1) DEFAULT 1,
  `user_date_created` datetime NOT NULL,
  `user_date_modified` datetime NOT NULL,
  `user_language` varchar(255) DEFAULT 'system',
  `user_name` text DEFAULT NULL,
  `user_company` text DEFAULT NULL,
  `user_address_1` text DEFAULT NULL,
  `user_address_2` text DEFAULT NULL,
  `user_city` text DEFAULT NULL,
  `user_state` text DEFAULT NULL,
  `user_zip` text DEFAULT NULL,
  `user_country` text DEFAULT NULL,
  `user_phone` text DEFAULT NULL,
  `user_fax` text DEFAULT NULL,
  `user_mobile` text DEFAULT NULL,
  `user_email` text DEFAULT NULL,
  `user_password` varchar(60) NOT NULL,
  `user_web` text DEFAULT NULL,
  `user_vat_id` text DEFAULT NULL,
  `user_tax_code` text DEFAULT NULL,
  `user_psalt` text DEFAULT NULL,
  `user_all_clients` int(1) NOT NULL DEFAULT 0,
  `user_passwordreset_token` varchar(100) DEFAULT '',
  `user_subscribernumber` varchar(40) DEFAULT NULL,
  `user_iban` varchar(34) DEFAULT NULL,
  `user_gln` bigint(13) DEFAULT NULL,
  `user_rcc` varchar(7) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `ip_users`
--

INSERT INTO `ip_users` (`user_id`, `user_type`, `user_active`, `user_date_created`, `user_date_modified`, `user_language`, `user_name`, `user_company`, `user_address_1`, `user_address_2`, `user_city`, `user_state`, `user_zip`, `user_country`, `user_phone`, `user_fax`, `user_mobile`, `user_email`, `user_password`, `user_web`, `user_vat_id`, `user_tax_code`, `user_psalt`, `user_all_clients`, `user_passwordreset_token`, `user_subscribernumber`, `user_iban`, `user_gln`, `user_rcc`) VALUES
(1, 1, 1, '2022-12-13 07:24:01', '2025-02-12 04:48:51', 'Australian-English', 'Aptitude Technology ', '', '11 Thompson st', 'Ascot', 'Perth', 'WA', '6104', 'AU', '(08) 9386 0020', '', '0404978533', 'chris@aptitudetech.com.au', '$2a$10$f9538f0d8afc95efda67deCVsRWKtUcsPJgsNJZ6omRoTTzg4K/UO', 'http://www.aptitudetech.com.au', '32680417314', '', 'f9538f0d8afc95efda67de', 0, '', '', '', NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `ip_user_clients`
--

CREATE TABLE `ip_user_clients` (
  `user_client_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `client_id` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `ip_user_custom`
--

CREATE TABLE `ip_user_custom` (
  `user_custom_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `user_custom_fieldid` int(11) NOT NULL,
  `user_custom_fieldvalue` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `ip_versions`
--

CREATE TABLE `ip_versions` (
  `version_id` int(11) NOT NULL,
  `version_date_applied` varchar(14) NOT NULL,
  `version_file` varchar(45) NOT NULL,
  `version_sql_errors` int(2) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `ip_versions`
--

INSERT INTO `ip_versions` (`version_id`, `version_date_applied`, `version_file`, `version_sql_errors`) VALUES
(1, '1670916124', '000_1.0.0.sql', 0),
(2, '1670916126', '001_1.0.1.sql', 0),
(3, '1670916126', '002_1.0.2.sql', 0),
(4, '1670916127', '003_1.1.0.sql', 0),
(5, '1670916127', '004_1.1.1.sql', 0),
(6, '1670916127', '005_1.1.2.sql', 0),
(7, '1670916127', '006_1.2.0.sql', 0),
(8, '1670916127', '007_1.2.1.sql', 0),
(9, '1670916127', '008_1.3.0.sql', 0),
(10, '1670916127', '009_1.3.1.sql', 0),
(11, '1670916127', '010_1.3.2.sql', 0),
(12, '1670916127', '011_1.3.3.sql', 0),
(13, '1670916127', '012_1.4.0.sql', 0),
(14, '1670916127', '013_1.4.1.sql', 0),
(15, '1670916127', '014_1.4.2.sql', 0),
(16, '1670916127', '015_1.4.3.sql', 0),
(17, '1670916127', '016_1.4.4.sql', 0),
(18, '1670916127', '017_1.4.5.sql', 0),
(19, '1670916127', '018_1.4.6.sql', 0),
(20, '1670916129', '019_1.4.7.sql', 0),
(21, '1670916131', '020_1.4.8.sql', 0),
(22, '1670916131', '021_1.4.9.sql', 0),
(23, '1670916131', '022_1.4.10.sql', 0),
(24, '1670916131', '023_1.5.0.sql', 0),
(25, '1670916132', '024_1.5.1.sql', 0),
(26, '1670916132', '025_1.5.2.sql', 0),
(27, '1670916132', '026_1.5.3.sql', 0),
(28, '1670916132', '027_1.5.4.sql', 0),
(29, '1670916132', '028_1.5.5.sql', 0),
(30, '1670916132', '029_1.5.6.sql', 0),
(31, '1670916132', '030_1.5.7.sql', 0),
(32, '1670916132', '031_1.5.8.sql', 0),
(33, '1670916132', '032_1.5.9.sql', 0),
(34, '1670916132', '033_1.5.10.sql', 0),
(35, '1670916132', '034_1.5.11.sql', 0),
(36, '1670916132', '035_1.5.12.sql', 0),
(37, '1670916132', '036_1.6.sql', 0);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `ip_clients`
--
ALTER TABLE `ip_clients`
  ADD PRIMARY KEY (`client_id`),
  ADD KEY `client_active` (`client_active`);

--
-- Indexes for table `ip_client_custom`
--
ALTER TABLE `ip_client_custom`
  ADD PRIMARY KEY (`client_custom_id`),
  ADD UNIQUE KEY `client_id` (`client_id`,`client_custom_fieldid`);

--
-- Indexes for table `ip_client_notes`
--
ALTER TABLE `ip_client_notes`
  ADD PRIMARY KEY (`client_note_id`),
  ADD KEY `client_id` (`client_id`,`client_note_date`);

--
-- Indexes for table `ip_custom_fields`
--
ALTER TABLE `ip_custom_fields`
  ADD PRIMARY KEY (`custom_field_id`),
  ADD UNIQUE KEY `custom_field_table_2` (`custom_field_table`,`custom_field_label`),
  ADD KEY `custom_field_table` (`custom_field_table`);

--
-- Indexes for table `ip_custom_values`
--
ALTER TABLE `ip_custom_values`
  ADD PRIMARY KEY (`custom_values_id`);

--
-- Indexes for table `ip_email_templates`
--
ALTER TABLE `ip_email_templates`
  ADD PRIMARY KEY (`email_template_id`);

--
-- Indexes for table `ip_families`
--
ALTER TABLE `ip_families`
  ADD PRIMARY KEY (`family_id`);

--
-- Indexes for table `ip_imports`
--
ALTER TABLE `ip_imports`
  ADD PRIMARY KEY (`import_id`);

--
-- Indexes for table `ip_import_details`
--
ALTER TABLE `ip_import_details`
  ADD PRIMARY KEY (`import_detail_id`),
  ADD KEY `import_id` (`import_id`,`import_record_id`);

--
-- Indexes for table `ip_invoices`
--
ALTER TABLE `ip_invoices`
  ADD PRIMARY KEY (`invoice_id`),
  ADD UNIQUE KEY `invoice_url_key` (`invoice_url_key`),
  ADD KEY `user_id` (`user_id`,`client_id`,`invoice_group_id`,`invoice_date_created`,`invoice_date_due`,`invoice_number`),
  ADD KEY `invoice_status_id` (`invoice_status_id`);

--
-- Indexes for table `ip_invoices_recurring`
--
ALTER TABLE `ip_invoices_recurring`
  ADD PRIMARY KEY (`invoice_recurring_id`),
  ADD KEY `invoice_id` (`invoice_id`);

--
-- Indexes for table `ip_invoice_amounts`
--
ALTER TABLE `ip_invoice_amounts`
  ADD PRIMARY KEY (`invoice_amount_id`),
  ADD KEY `invoice_id` (`invoice_id`),
  ADD KEY `invoice_paid` (`invoice_paid`,`invoice_balance`);

--
-- Indexes for table `ip_invoice_custom`
--
ALTER TABLE `ip_invoice_custom`
  ADD PRIMARY KEY (`invoice_custom_id`),
  ADD UNIQUE KEY `invoice_id` (`invoice_id`,`invoice_custom_fieldid`);

--
-- Indexes for table `ip_invoice_groups`
--
ALTER TABLE `ip_invoice_groups`
  ADD PRIMARY KEY (`invoice_group_id`),
  ADD KEY `invoice_group_next_id` (`invoice_group_next_id`),
  ADD KEY `invoice_group_left_pad` (`invoice_group_left_pad`);

--
-- Indexes for table `ip_invoice_items`
--
ALTER TABLE `ip_invoice_items`
  ADD PRIMARY KEY (`item_id`),
  ADD KEY `invoice_id` (`invoice_id`,`item_tax_rate_id`,`item_date_added`,`item_order`);

--
-- Indexes for table `ip_invoice_item_amounts`
--
ALTER TABLE `ip_invoice_item_amounts`
  ADD PRIMARY KEY (`item_amount_id`),
  ADD KEY `item_id` (`item_id`);

--
-- Indexes for table `ip_invoice_sumex`
--
ALTER TABLE `ip_invoice_sumex`
  ADD PRIMARY KEY (`sumex_id`);

--
-- Indexes for table `ip_invoice_tax_rates`
--
ALTER TABLE `ip_invoice_tax_rates`
  ADD PRIMARY KEY (`invoice_tax_rate_id`),
  ADD KEY `invoice_id` (`invoice_id`,`tax_rate_id`);

--
-- Indexes for table `ip_item_lookups`
--
ALTER TABLE `ip_item_lookups`
  ADD PRIMARY KEY (`item_lookup_id`);

--
-- Indexes for table `ip_login_log`
--
ALTER TABLE `ip_login_log`
  ADD PRIMARY KEY (`login_name`);

--
-- Indexes for table `ip_merchant_responses`
--
ALTER TABLE `ip_merchant_responses`
  ADD PRIMARY KEY (`merchant_response_id`),
  ADD KEY `merchant_response_date` (`merchant_response_date`),
  ADD KEY `invoice_id` (`invoice_id`);

--
-- Indexes for table `ip_payments`
--
ALTER TABLE `ip_payments`
  ADD PRIMARY KEY (`payment_id`),
  ADD KEY `invoice_id` (`invoice_id`),
  ADD KEY `payment_method_id` (`payment_method_id`),
  ADD KEY `payment_amount` (`payment_amount`);

--
-- Indexes for table `ip_payment_custom`
--
ALTER TABLE `ip_payment_custom`
  ADD PRIMARY KEY (`payment_custom_id`),
  ADD UNIQUE KEY `payment_id` (`payment_id`,`payment_custom_fieldid`);

--
-- Indexes for table `ip_payment_methods`
--
ALTER TABLE `ip_payment_methods`
  ADD PRIMARY KEY (`payment_method_id`);

--
-- Indexes for table `ip_products`
--
ALTER TABLE `ip_products`
  ADD PRIMARY KEY (`product_id`);

--
-- Indexes for table `ip_projects`
--
ALTER TABLE `ip_projects`
  ADD PRIMARY KEY (`project_id`);

--
-- Indexes for table `ip_quotes`
--
ALTER TABLE `ip_quotes`
  ADD PRIMARY KEY (`quote_id`),
  ADD KEY `user_id` (`user_id`,`client_id`,`invoice_group_id`,`quote_date_created`,`quote_date_expires`,`quote_number`),
  ADD KEY `invoice_id` (`invoice_id`),
  ADD KEY `quote_status_id` (`quote_status_id`);

--
-- Indexes for table `ip_quote_amounts`
--
ALTER TABLE `ip_quote_amounts`
  ADD PRIMARY KEY (`quote_amount_id`),
  ADD KEY `quote_id` (`quote_id`);

--
-- Indexes for table `ip_quote_custom`
--
ALTER TABLE `ip_quote_custom`
  ADD PRIMARY KEY (`quote_custom_id`),
  ADD UNIQUE KEY `quote_id` (`quote_id`,`quote_custom_fieldid`);

--
-- Indexes for table `ip_quote_items`
--
ALTER TABLE `ip_quote_items`
  ADD PRIMARY KEY (`item_id`),
  ADD KEY `quote_id` (`quote_id`,`item_date_added`,`item_order`),
  ADD KEY `item_tax_rate_id` (`item_tax_rate_id`);

--
-- Indexes for table `ip_quote_item_amounts`
--
ALTER TABLE `ip_quote_item_amounts`
  ADD PRIMARY KEY (`item_amount_id`),
  ADD KEY `item_id` (`item_id`);

--
-- Indexes for table `ip_quote_tax_rates`
--
ALTER TABLE `ip_quote_tax_rates`
  ADD PRIMARY KEY (`quote_tax_rate_id`),
  ADD KEY `quote_id` (`quote_id`),
  ADD KEY `tax_rate_id` (`tax_rate_id`);

--
-- Indexes for table `ip_sessions`
--
ALTER TABLE `ip_sessions`
  ADD KEY `ip_sessions_timestamp` (`timestamp`);

--
-- Indexes for table `ip_settings`
--
ALTER TABLE `ip_settings`
  ADD PRIMARY KEY (`setting_id`),
  ADD KEY `setting_key` (`setting_key`);

--
-- Indexes for table `ip_tasks`
--
ALTER TABLE `ip_tasks`
  ADD PRIMARY KEY (`task_id`);

--
-- Indexes for table `ip_tax_rates`
--
ALTER TABLE `ip_tax_rates`
  ADD PRIMARY KEY (`tax_rate_id`);

--
-- Indexes for table `ip_units`
--
ALTER TABLE `ip_units`
  ADD PRIMARY KEY (`unit_id`);

--
-- Indexes for table `ip_uploads`
--
ALTER TABLE `ip_uploads`
  ADD PRIMARY KEY (`upload_id`);

--
-- Indexes for table `ip_users`
--
ALTER TABLE `ip_users`
  ADD PRIMARY KEY (`user_id`);

--
-- Indexes for table `ip_user_clients`
--
ALTER TABLE `ip_user_clients`
  ADD PRIMARY KEY (`user_client_id`),
  ADD KEY `user_id` (`user_id`,`client_id`);

--
-- Indexes for table `ip_user_custom`
--
ALTER TABLE `ip_user_custom`
  ADD PRIMARY KEY (`user_custom_id`),
  ADD UNIQUE KEY `user_id` (`user_id`,`user_custom_fieldid`);

--
-- Indexes for table `ip_versions`
--
ALTER TABLE `ip_versions`
  ADD PRIMARY KEY (`version_id`),
  ADD KEY `version_date_applied` (`version_date_applied`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `ip_clients`
--
ALTER TABLE `ip_clients`
  MODIFY `client_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=46;

--
-- AUTO_INCREMENT for table `ip_client_custom`
--
ALTER TABLE `ip_client_custom`
  MODIFY `client_custom_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=46;

--
-- AUTO_INCREMENT for table `ip_client_notes`
--
ALTER TABLE `ip_client_notes`
  MODIFY `client_note_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `ip_custom_fields`
--
ALTER TABLE `ip_custom_fields`
  MODIFY `custom_field_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `ip_custom_values`
--
ALTER TABLE `ip_custom_values`
  MODIFY `custom_values_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `ip_email_templates`
--
ALTER TABLE `ip_email_templates`
  MODIFY `email_template_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `ip_families`
--
ALTER TABLE `ip_families`
  MODIFY `family_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT for table `ip_imports`
--
ALTER TABLE `ip_imports`
  MODIFY `import_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `ip_import_details`
--
ALTER TABLE `ip_import_details`
  MODIFY `import_detail_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `ip_invoices`
--
ALTER TABLE `ip_invoices`
  MODIFY `invoice_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=90;

--
-- AUTO_INCREMENT for table `ip_invoices_recurring`
--
ALTER TABLE `ip_invoices_recurring`
  MODIFY `invoice_recurring_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `ip_invoice_amounts`
--
ALTER TABLE `ip_invoice_amounts`
  MODIFY `invoice_amount_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=90;

--
-- AUTO_INCREMENT for table `ip_invoice_custom`
--
ALTER TABLE `ip_invoice_custom`
  MODIFY `invoice_custom_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `ip_invoice_groups`
--
ALTER TABLE `ip_invoice_groups`
  MODIFY `invoice_group_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `ip_invoice_items`
--
ALTER TABLE `ip_invoice_items`
  MODIFY `item_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=129;

--
-- AUTO_INCREMENT for table `ip_invoice_item_amounts`
--
ALTER TABLE `ip_invoice_item_amounts`
  MODIFY `item_amount_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=129;

--
-- AUTO_INCREMENT for table `ip_invoice_sumex`
--
ALTER TABLE `ip_invoice_sumex`
  MODIFY `sumex_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `ip_invoice_tax_rates`
--
ALTER TABLE `ip_invoice_tax_rates`
  MODIFY `invoice_tax_rate_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `ip_item_lookups`
--
ALTER TABLE `ip_item_lookups`
  MODIFY `item_lookup_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `ip_merchant_responses`
--
ALTER TABLE `ip_merchant_responses`
  MODIFY `merchant_response_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `ip_payments`
--
ALTER TABLE `ip_payments`
  MODIFY `payment_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=55;

--
-- AUTO_INCREMENT for table `ip_payment_custom`
--
ALTER TABLE `ip_payment_custom`
  MODIFY `payment_custom_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `ip_payment_methods`
--
ALTER TABLE `ip_payment_methods`
  MODIFY `payment_method_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `ip_products`
--
ALTER TABLE `ip_products`
  MODIFY `product_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=51;

--
-- AUTO_INCREMENT for table `ip_projects`
--
ALTER TABLE `ip_projects`
  MODIFY `project_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `ip_quotes`
--
ALTER TABLE `ip_quotes`
  MODIFY `quote_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `ip_quote_amounts`
--
ALTER TABLE `ip_quote_amounts`
  MODIFY `quote_amount_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `ip_quote_custom`
--
ALTER TABLE `ip_quote_custom`
  MODIFY `quote_custom_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `ip_quote_items`
--
ALTER TABLE `ip_quote_items`
  MODIFY `item_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=40;

--
-- AUTO_INCREMENT for table `ip_quote_item_amounts`
--
ALTER TABLE `ip_quote_item_amounts`
  MODIFY `item_amount_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=40;

--
-- AUTO_INCREMENT for table `ip_quote_tax_rates`
--
ALTER TABLE `ip_quote_tax_rates`
  MODIFY `quote_tax_rate_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `ip_settings`
--
ALTER TABLE `ip_settings`
  MODIFY `setting_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=96;

--
-- AUTO_INCREMENT for table `ip_tasks`
--
ALTER TABLE `ip_tasks`
  MODIFY `task_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `ip_tax_rates`
--
ALTER TABLE `ip_tax_rates`
  MODIFY `tax_rate_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `ip_units`
--
ALTER TABLE `ip_units`
  MODIFY `unit_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `ip_uploads`
--
ALTER TABLE `ip_uploads`
  MODIFY `upload_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `ip_users`
--
ALTER TABLE `ip_users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `ip_user_clients`
--
ALTER TABLE `ip_user_clients`
  MODIFY `user_client_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `ip_user_custom`
--
ALTER TABLE `ip_user_custom`
  MODIFY `user_custom_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `ip_versions`
--
ALTER TABLE `ip_versions`
  MODIFY `version_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=38;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
