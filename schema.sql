--
-- PostgreSQL database dump
--

-- Dumped from database version 10.3
-- Dumped by pg_dump version 10.3

-- Started on 2018-09-30 23:06:07

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 1 (class 3079 OID 12924)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- TOC entry 2813 (class 0 OID 0)
-- Dependencies: 1
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 197 (class 1259 OID 24583)
-- Name: dept; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.dept (
    employee character varying(30) NOT NULL,
    department character varying(30) NOT NULL,
    valid_from date NOT NULL,
    valid_to date NOT NULL
);


ALTER TABLE public.dept OWNER TO postgres;

--
-- TOC entry 196 (class 1259 OID 24578)
-- Name: emp; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.emp (
    instance character varying(30) NOT NULL,
    name character varying(30) NOT NULL,
    valid_from date NOT NULL,
    valid_to date NOT NULL
);


ALTER TABLE public.emp OWNER TO postgres;

--
-- TOC entry 198 (class 1259 OID 24588)
-- Name: mgr; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mgr (
    name character varying(30) NOT NULL,
    department character varying(30) NOT NULL,
    valid_from date NOT NULL,
    valid_to date NOT NULL
);


ALTER TABLE public.mgr OWNER TO postgres;

--
-- TOC entry 2804 (class 0 OID 24583)
-- Dependencies: 197
-- Data for Name: dept; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.dept (employee, department, valid_from, valid_to) FROM stdin;
\.


--
-- TOC entry 2803 (class 0 OID 24578)
-- Dependencies: 196
-- Data for Name: emp; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.emp (instance, name, valid_from, valid_to) FROM stdin;
\.


--
-- TOC entry 2805 (class 0 OID 24588)
-- Dependencies: 198
-- Data for Name: mgr; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mgr (name, department, valid_from, valid_to) FROM stdin;
\.


--
-- TOC entry 2679 (class 2606 OID 24587)
-- Name: dept dept_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dept
    ADD CONSTRAINT dept_pkey PRIMARY KEY (employee, department, valid_from, valid_to);


--
-- TOC entry 2677 (class 2606 OID 24582)
-- Name: emp emp_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.emp
    ADD CONSTRAINT emp_pkey PRIMARY KEY (instance, name, valid_from, valid_to);


--
-- TOC entry 2681 (class 2606 OID 24592)
-- Name: mgr mgr_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mgr
    ADD CONSTRAINT mgr_pkey PRIMARY KEY (valid_to, valid_from, department, name);


-- Completed on 2018-09-30 23:06:07

--
-- PostgreSQL database dump complete
--

