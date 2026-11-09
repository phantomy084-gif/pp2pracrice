CREATE OR REPLACE FUNCTION search_contacts(pattern TEXT)
RETURNS TABLE (
    id INTEGER,
    first_name VARCHAR(100),
    phone VARCHAR(20)
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT c.id, c.first_name, c.phone
    FROM contacts AS c
    WHERE c.first_name ILIKE '%' || pattern || '%'
       OR c.phone LIKE '%' || pattern || '%';
END;
$$;

CREATE OR REPLACE FUNCTION get_contacts_page(
    p_limit INTEGER,
    p_offset INTEGER
)
RETURNS TABLE (
    id INTEGER,
    first_name VARCHAR(100),
    phone VARCHAR(20)
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT c.id, c.first_name, c.phone
    FROM contacts AS c
    ORDER BY c.id
    LIMIT p_limit
    OFFSET p_offset;
END;
$$;