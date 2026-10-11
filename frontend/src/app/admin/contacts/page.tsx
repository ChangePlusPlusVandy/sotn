import { auth } from "@clerk/nextjs/server";

const ContactsPage = async () => {
  await auth.protect();

  return (
    <>
      <h1 className="text-2xl font-semibold">Contacts</h1>
      <p>TODO: Routed athletes, guardians, volunteers, donors and orgs, with last touch and a Log touch button.</p>
    </>
  );
};

export default ContactsPage;
