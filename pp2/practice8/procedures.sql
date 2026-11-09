CREATE OR REPLACE PROCEDURE insert_or_update_user(
    p_name VARCHAR(100),
    p_phone VARCHAR(20)
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM contacts
        WHERE first_name = p_name
    ) THEN
        UPDATE contacts
        SET phone = p_phone
        WHERE first_name = p_name;

    ELSE
        INSERT INTO contacts (first_name, phone)
        VALUES (p_name, p_phone);
    END IF;
END;
$$;
CREATE OR REPLACE PROCEDURE insert_many_users(
    p_names TEXT[],
    p_phones TEXT[],
    INOUT p_invalid_data TEXT
)
LANGUAGE plpgsql
AS $$
DECLARE
    i INTEGER;
    total INTEGER;
    v_name TEXT;
    v_phone TEXT;
BEGIN
    p_invalid_data := '';

    total := GREATEST(
        COALESCE(array_length(p_names, 1), 0),
        COALESCE(array_length(p_phones, 1), 0)
    );

    IF total > 0 THEN
        FOR i IN 1..total LOOP

            v_name := p_names[i];
            v_phone := p_phones[i];

            IF v_name IS NULL OR TRIM(v_name) = ''
               OR v_phone IS NULL
               OR v_phone !~ '^\+[0-9]{11}$' THEN

                p_invalid_data := p_invalid_data ||
                    'Invalid data: ' ||
                    COALESCE(v_name, 'No name') || ' - ' ||
                    COALESCE(v_phone, 'No phone') || E'\n';

            ELSE
                INSERT INTO contacts (first_name, phone)
                VALUES (v_name, v_phone)
                ON CONFLICT (phone) DO NOTHING;
            END IF;

        END LOOP;
    END IF;
END;
$$;