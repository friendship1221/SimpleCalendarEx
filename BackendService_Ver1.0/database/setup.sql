# Database setup script
# Run this SQL in your PostgreSQL database to create the required table

-- Drop table if exists
-- DROP TABLE IF EXISTS public.daysoffyear;

CREATE TABLE public.daysoffyear (
	id uuid NOT NULL,
	organid varchar(250),
	dayoff date NULL,
	"year" int4 NULL,
	description text NULL,
	creator varchar(250) NULL,
	createdate date NULL,
	modifier varchar(250) NULL,
	modifydate date NULL,
	delflag int4 NULL DEFAULT 0,
	CONSTRAINT daysoffyear_pkey PRIMARY KEY (id)
);

-- Create indexes for better performance
CREATE INDEX idx_daysoffyear_organid ON public.daysoffyear(organid);
CREATE INDEX idx_daysoffyear_dayoff ON public.daysoffyear(organid,dayoff);
CREATE INDEX idx_daysoffyear_delflag ON public.daysoffyear(organid,dayoff,delflag);

-- Permissions
ALTER TABLE public.daysoffyear OWNER TO postgres;
GRANT ALL ON TABLE public.daysoffyear TO postgres;