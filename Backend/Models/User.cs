using System.ComponentModel.DataAnnotations;

namespace NagyprojektBackend.Models
{
    public class User
    {
        [Key]
        public int Id { get; set; }
        [Required]
        public string Username { get; set; } = null!;
        [Required]
        public string PasswordHash { get; set; } = null!; // egyszerű hash példa
        public string? DisplayName { get; set; }
        public string? Email { get; set; }
        public string? Role { get; set; }
    }
}
