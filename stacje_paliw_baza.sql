PGDMP  .                    }           stacje_paliw    16.2    16.2     �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    37773    stacje_paliw    DATABASE        CREATE DATABASE stacje_paliw WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Polish_Poland.1250';
    DROP DATABASE stacje_paliw;
                postgres    false                        3079    37774    postgis 	   EXTENSION     ;   CREATE EXTENSION IF NOT EXISTS postgis WITH SCHEMA public;
    DROP EXTENSION postgis;
                   false            �           0    0    EXTENSION postgis    COMMENT     ^   COMMENT ON EXTENSION postgis IS 'PostGIS geometry and geography spatial types and functions';
                        false    2            �            1259    38851    stacje_paliw    TABLE     `  CREATE TABLE public.stacje_paliw (
    id integer NOT NULL,
    nazwa_stacji character varying(100),
    adres character varying(200),
    dzielnica character varying(100),
    pb95 numeric(4,2),
    pb98 numeric(4,2),
    diesel numeric(4,2),
    lpg numeric(4,2),
    geom public.geometry(Point,2180),
    lat numeric(12,6),
    lon numeric(12,6)
);
     DROP TABLE public.stacje_paliw;
       public         heap    postgres    false    2    2    2    2    2    2    2    2            �            1259    38850    stacje_paliw_id_seq    SEQUENCE     �   CREATE SEQUENCE public.stacje_paliw_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public.stacje_paliw_id_seq;
       public          postgres    false    222            �           0    0    stacje_paliw_id_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public.stacje_paliw_id_seq OWNED BY public.stacje_paliw.id;
          public          postgres    false    221            �           2604    38854    stacje_paliw id    DEFAULT     r   ALTER TABLE ONLY public.stacje_paliw ALTER COLUMN id SET DEFAULT nextval('public.stacje_paliw_id_seq'::regclass);
 >   ALTER TABLE public.stacje_paliw ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    221    222    222            �          0    38092    spatial_ref_sys 
   TABLE DATA           X   COPY public.spatial_ref_sys (srid, auth_name, auth_srid, srtext, proj4text) FROM stdin;
    public          postgres    false    217   �       �          0    38851    stacje_paliw 
   TABLE DATA           s   COPY public.stacje_paliw (id, nazwa_stacji, adres, dzielnica, pb95, pb98, diesel, lpg, geom, lat, lon) FROM stdin;
    public          postgres    false    222   �       �           0    0    stacje_paliw_id_seq    SEQUENCE SET     B   SELECT pg_catalog.setval('public.stacje_paliw_id_seq', 68, true);
          public          postgres    false    221            �           2606    38858    stacje_paliw stacje_paliw_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.stacje_paliw
    ADD CONSTRAINT stacje_paliw_pkey PRIMARY KEY (id);
 H   ALTER TABLE ONLY public.stacje_paliw DROP CONSTRAINT stacje_paliw_pkey;
       public            postgres    false    222            �      x������ � �      �   �  x��Z�n\׵��������yv"[xr" ��*S%S��"�r($���0�����s���t��@P2���nV�Kj��w�on^m�o�x<<����]��P�y{�w�������Q���K�Ř{e�P���AL�.:���I8���$KQ0jit#�+��6dC��p�������n�i�[������������l�+�������:ȬM���XB�"�}�rZC���ƿYy�|�����OW��pQ^^�(�ӵ�,ee�0�+Y��=�!%E��k�ZtJ���?�\b�[f�����p}�?<��R�_��B���̉`�t�������T�liBS�ѵZs�$�(c�e~FxJ�yץ.�/�ҋ�R���q�래䩖LG?f��R���Bt���w��8)�*mתd�0vV�%���F�\hcg��R��L@�z_���8��wׇ��/���{���������B�^p�J��10�%�Wʙ��1\���D�ԭJQj:�7����]K�<o�WH�?+�@�j�N����)!�0N�B���Z>�7c��sEdG�"�_����}/�����SYIƷzi��gas����(�����ؤ[h�DG��}�_m���x�Ԇ����zXEP������Ls`���0&����+)��5�taJAKbU{�ŒtTO������L�*�e>�Y�,5A{OJdM"P.����#�Z�=�t�l��xu�����ϻ��e�W�:NI��+�HU:���,()�Вp$�Ν$��⒄QDc�&j����-�gZ.���2���Z�2�d 1*G���e�8�1�y�qwsS�`��q|�Bxl���V �Eelɂ�I�kxD�6�72�fX��RKc͔��Ȓ�E�������<���
+j�0�J�N����QQ��[&T��`�� ��;5W��c�p�p�"|��"V@W*�%:_{=�pF����>� �0=EWL���:�`�(�YN�(;`�
Y���M �JZ����F��ph�����ܢC!�����?�!�x���=�F*F�'�
l�����k(�%>+����B'gC�! s��$��)����r��$���o�)%�j\D��GDH�y��P�H$s��1%*�8d
���E~<���� z�b��Y�����>��S��0 QGmx"� (\Ѣ���+ �k�yw�����|)�*UA$y���d�p���:��Db�0l��p.*X!��:��\�Ex1� h��m��k������3���ĸd".m� �@X��ׇ�������Yy��m	���6 ����+	A��0�l��B�!:2�����}�������S��*"0�Ez�&�V*��(�hjLb�k|� �LO�������Ça	Q�S"`�m����}�BP"T��Ce З0�� B�A�u|����fWY��|~z<<�&̙.�r䥊�v�'�D�_��&�� z�	Xy�~f�&����<�";]˪�nb��H��f�!��s%�L"7���y�͸m�'!H~[��C_��r"��)��}NA}"d�%rĐzUh�,�u�L�l)��@����c�?<���2�J��iCV ae ����9�J�DP|��!/$�f���) �4�������U,E�k�\�m��p� ,Õ�T�� �p�> [��:�\�]�o�`1��o�ݲ(�. .U VbC�DdI��Ff���X2���@�/�pLa�����2tM�i�����6<[��R���Gju�R2$a�"�wh�s�­���^@?j��%�J�@�?�I�m+�����<���0�g�b�F#v�?�����iK�mc�*��b"sD�,6�At �iYf�eƦ�����vb��?�\��/��/����^ia�#	8c%�a<0�4�ZhԀ.m]�I���� }$[�@$W�*�6���<D�Jub���_pBu&��]s��@8����	��{��͉�.�g��H�ÂM��vw|_�|��G�Ep�Kx����+�R��)��N��ah��~�� �F�.�{�{͹	AU�����Qj�*�ʨ�R�~8���0�F��%��^��{N��b�������0$qQl�.�K"Q��)�����w)uN�3���պS�@Fy�YH�u6�$DnV n%7�u7�O������C�=����~�_
26y�rkC�R,}���e�e�f���	�4K`�M��>.�q�F���~x,`F9)�g�N��|�
dKE	úb@��̻�˗�Q�Hr?�� ��I������tn��<�8�2�Y�!ۡ���dG'���~�Sᣗ펇���x����P��C/�a�R�$�U��	)>4Ô�0�`�;�}\�7Ѓ�&�[7J�t(�����*�%�xm��xgsN~&!�e������/�?�|�D	���+����ˁ��	����J�0ueW��9^���-��ٱ�̡*1�K.Ѱb��5�V7D`IlH8d�6�`������?����ߜ����G*W��9g\�NYӠA)C<6t��ޤ����d!�ms�w���y�/ViwW��E_�j��N�U\K����|Z�$��*Y�qV�괐FS6xeNm'�I|���P	uv�0uj�Տ, �l,�,V��1���0���Om2�X6��9����c=֞K�j+�s��5���>нs�Q������LE(����˷n8����_yܲ�Ca=T��P���EP2$G��D,� al�]�����!�h'�,ɻç�}�YǢ���N���I�AF$A����h�������!	e'������/xwi���VeN+�]`k`1F=�8���(�5D4e!�&C)�F��t����s;ꌜ�x�4^8�	�!�y����Ip	� �����L=A�:���owϏ��b)M�Y��U�d��p����i����0�S?� d�EF;���@�����"�M/�Ȣ��B[lf��Y�`��ru�S&/X��'5�??��$|�Jl�GS�v�d�2A7���JN@6���T�x+���7#E��χǊ�ϳ�^����U��৐v!���&@��HNTk5��V������s���;/_���;��*8Þ	i�e)��Ƀ/g>�Z�T�e �)�;�H{:AŬ���!�0�B��r3N�\0�Κ	��}��T����b*�5�g���ZY��I�40�r���&;)��ϛR�!a��ӧ\���z���~^> \�	�����������e�A�A�?�4������ҭ X����C���2���H��2h���$I�
c�^6�͉�?:��{c�}ZYH��tQE�B���S�tFh��(�p�b��L=�ޏ�3urc���J�������惤��\Sf�_-��`r�#0�]�e�щiS���n����2S����`���>�9�"�}��^pN�����?���     