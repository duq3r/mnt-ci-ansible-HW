netology86-role
=========

Requirements
------------

None

Role Variables
--------------

  - `file_path`: path to file
  - `file_content`: content for the file

Dependencies
------------

None

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - name: Create test file
      vars:
        - file_path: "~/file.txt"
        - file_content: "Simple text"
      roles: 
        - netology86-role

License
-------

MIT

