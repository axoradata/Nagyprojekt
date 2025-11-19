using System.ComponentModel.DataAnnotations;

namespace NagyprojektBackend.Models
{
    public class Group
    {
        [Key]
        public int Id { get; set; }
        public string Name { get; set; } = null!;
        public string? Description { get; set; }
    }
}
