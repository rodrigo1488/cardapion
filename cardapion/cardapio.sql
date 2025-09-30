-- WARNING: This schema is for context only and is not meant to be run.
-- Table order and constraints may not be valid for execution.

CREATE TABLE public.categories_products (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  name text,
  id_company uuid,
  kitchen boolean DEFAULT true,
  CONSTRAINT categories_products_pkey PRIMARY KEY (id),
  CONSTRAINT categories_id_company_fkey FOREIGN KEY (id_company) REFERENCES public.company(id)
);
CREATE TABLE public.client (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  name text,
  email text NOT NULL,
  adress_1 text,
  adres_2 text,
  contact numeric,
  cpf_cnpj numeric NOT NULL,
  CONSTRAINT client_pkey PRIMARY KEY (email, id, cpf_cnpj)
);
CREATE TABLE public.company (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  name text,
  cnpj text,
  email text,
  adress text,
  contact numeric,
  status_acess boolean DEFAULT false,
  CONSTRAINT company_pkey PRIMARY KEY (id)
);
CREATE TABLE public.delivery (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  id_client uuid,
  id_company uuid,
  status text,
  id_payment uuid,
  CONSTRAINT delivery_pkey PRIMARY KEY (id),
  CONSTRAINT delivery_id_company_fkey FOREIGN KEY (id_company) REFERENCES public.company(id),
  CONSTRAINT delivery_id_payment_fkey FOREIGN KEY (id_payment) REFERENCES public.payments(id)
);
CREATE TABLE public.order_product (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  id_product uuid,
  id_order uuid,
  id_company uuid,
  CONSTRAINT order_product_pkey PRIMARY KEY (id),
  CONSTRAINT order_product_id_order_fkey FOREIGN KEY (id_order) REFERENCES public.orders(id),
  CONSTRAINT order_product_id_company_fkey FOREIGN KEY (id_company) REFERENCES public.company(id),
  CONSTRAINT order_product_id_product_fkey FOREIGN KEY (id_product) REFERENCES public.products(id)
);
CREATE TABLE public.orders (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  id_table uuid,
  id_order_delivery uuid DEFAULT gen_random_uuid(),
  value numeric,
  id_company uuid,
  is_delivery boolean NOT NULL,
  is_table boolean,
  CONSTRAINT orders_pkey PRIMARY KEY (id),
  CONSTRAINT orders_id_table_fkey FOREIGN KEY (id_table) REFERENCES public.tables(id),
  CONSTRAINT orders_id_company_fkey FOREIGN KEY (id_company) REFERENCES public.company(id),
  CONSTRAINT orders_id_order_delivery_fkey FOREIGN KEY (id_order_delivery) REFERENCES public.delivery(id)
);
CREATE TABLE public.orders_finished (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  id_company uuid DEFAULT gen_random_uuid(),
  id_order uuid DEFAULT gen_random_uuid(),
  value numeric,
  CONSTRAINT orders_finished_pkey PRIMARY KEY (id),
  CONSTRAINT orders_finished_id_company_fkey FOREIGN KEY (id_company) REFERENCES public.company(id),
  CONSTRAINT orders_finished_id_order_fkey FOREIGN KEY (id_order) REFERENCES public.orders(id)
);
CREATE TABLE public.payment_companies (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  name text,
  id_company uuid,
  CONSTRAINT payment_companies_pkey PRIMARY KEY (id),
  CONSTRAINT payment_companies_id_company_fkey FOREIGN KEY (id_company) REFERENCES public.company(id)
);
CREATE TABLE public.payments (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  name text,
  id_company uuid,
  CONSTRAINT payments_pkey PRIMARY KEY (id),
  CONSTRAINT payments_id_company_fkey FOREIGN KEY (id_company) REFERENCES public.company(id)
);
CREATE TABLE public.products (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  name text,
  price bigint,
  description text,
  id_company uuid,
  id_categorie uuid,
  preparation_time time without time zone,
  CONSTRAINT products_pkey PRIMARY KEY (id),
  CONSTRAINT products_id_company_fkey FOREIGN KEY (id_company) REFERENCES public.company(id),
  CONSTRAINT products_id_categorie_fkey FOREIGN KEY (id_categorie) REFERENCES public.categories_products(id)
);
CREATE TABLE public.requests_kitchen (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  id_company uuid,
  id_order uuid,
  CONSTRAINT requests_kitchen_pkey PRIMARY KEY (id),
  CONSTRAINT requests_kitchen_id_company_fkey FOREIGN KEY (id_company) REFERENCES public.company(id),
  CONSTRAINT requests_kitchen_id_order_fkey FOREIGN KEY (id_order) REFERENCES public.orders(id)
);
CREATE TABLE public.tables (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  id_company uuid,
  number_table bigint,
  status text DEFAULT 'free'::text,
  id_client uuid,
  id_order uuid,
  CONSTRAINT tables_pkey PRIMARY KEY (id),
  CONSTRAINT tables_id_company_fkey FOREIGN KEY (id_company) REFERENCES public.company(id),
  CONSTRAINT tables_id_order_fkey FOREIGN KEY (id_order) REFERENCES public.orders(id)
);
CREATE TABLE public.users_company (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  name text,
  email text,
  password text,
  id_company uuid,
  CONSTRAINT users_company_pkey PRIMARY KEY (id),
  CONSTRAINT users_company_id_company_fkey FOREIGN KEY (id_company) REFERENCES public.company(id)
);